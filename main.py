import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
import os

BOOKMARKS_FILE = "bookmarks.json"


class TabWebEngineView(QWebEngineView):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def createWindow(self, _type):
        self.main_window.add_new_tab()
        return self.main_window.tabs.currentWidget()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gama Browser")

        self.history = []

        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.progress.setVisible(False)
        self.navbar.addWidget(self.progress)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.botoes(self.navbar)
        self.url_bar_widget(self.navbar)

        self.add_new_tab("https://google.com.br", "Home")
        self.show()

        QShortcut(QKeySequence("Ctrl+T"), self, self.add_new_tab)  # Nova aba
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.close_current_tab(self.tabs.currentIndex()))  # Fechar aba
        QShortcut(QKeySequence("Ctrl+Tab"), self, lambda: self.tabs.setCurrentIndex((self.tabs.currentIndex()+1)%self.tabs.count()))  # Próxima aba
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, lambda: self.tabs.setCurrentIndex((self.tabs.currentIndex()-1)%self.tabs.count()))  # Aba anterior

        self.load_bookmarks()
        bookmark_btn = QAction('⭐ Favoritar', self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        self.navbar.addAction(bookmark_btn)

        show_bookmarks_btn = QAction('📖 Favoritos', self)
        show_bookmarks_btn.triggered.connect(self.show_bookmarks)
        self.navbar.addAction(show_bookmarks_btn)


    # =====================
    # Funções de aba
    # =====================

    def add_new_tab(self, qurl=None, label="Nova Aba"):
        if qurl is None:
            qurl = "https://google.com.br"

        browser = TabWebEngineView(self)
        browser.setUrl(QUrl(qurl))

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.loadFinished.connect(lambda ok, i=i, b=browser: self.on_load_finished(i, b))

        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))

        browser.page().profile().downloadRequested.connect(self.on_download_requested)

    def on_load_finished(self, i, browser):
        self.tabs.setTabText(i, browser.page().title())
        self.add_to_history(browser)

    def add_to_history(self, browser):
        title = browser.page().title()
        url = browser.url().toString()
        self.history.append((title, url))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def current_tab_changed(self, i):
        if self.tabs.currentWidget():
            qurl = self.tabs.currentWidget().url()
            self.update_url(qurl, self.tabs.currentWidget())

    # =====================
    # Navbar
    # =====================

    def botoes(self, navbar):
        back_btn = QAction('<', self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('>', self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction('Recarregar', self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://google.com.br")))
        navbar.addAction(home_btn)

        new_tab_btn = QAction('Nova Aba', self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navbar.addAction(new_tab_btn)

        history_btn = QAction('Histórico', self)
        history_btn.triggered.connect(self.show_history)
        navbar.addAction(history_btn)

        theme_btn = QAction("Tema Escuro", self)
        theme_btn.triggered.connect(self.toggle_theme)
        self.navbar.addAction(theme_btn)
        self.dark_mode = False


    def url_bar_widget(self, navbar):
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

    def navigate_to_url(self):
        text = self.url_bar.text()
        if text.startswith("g "):
            query = text[2:]
            url = f"https://www.google.com/search?q={query}"
        elif text.startswith("w "):
            query = text[2:]
            url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        elif text.startswith("d "):
            query = text[2:]
            url = f"https://duckduckgo.com/?q={query}"
        else:
            url = text
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))


    def update_url(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())

    def toggle_theme(self):
        if not self.dark_mode:
            self.setStyleSheet("QMainWindow {background-color: #2b2b2b;} QToolBar {background-color: #3c3c3c;} QTabWidget::pane {background-color: #2b2b2b;} QLineEdit {background-color: #3c3c3c; color: white;}")
            self.dark_mode = True
        else:
            self.setStyleSheet("")
            self.dark_mode = False


    # =====================
    # Histórico
    # =====================

    def show_history(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Histórico de Navegação")
        layout = QVBoxLayout()

        list_widget = QListWidget()
        for title, url in reversed(self.history):
            list_widget.addItem(f"{title} - {url}")

        list_widget.itemDoubleClicked.connect(lambda item: self.open_history_item(item))

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()

    def open_history_item(self, item):
        url = item.text().split(" - ")[-1]
        self.add_new_tab(url, "Nova Aba")

    # =====================
    # Downloads
    # =====================

    def on_download_requested(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo", download.path())
        if path:
            download.setPath(path)
            download.accept()
            download.downloadProgress.connect(self.show_download_progress)

    def show_download_progress(self, received, total):
        if total > 0:
            self.progress.setVisible(True)
            self.progress.setMaximum(total)
            self.progress.setValue(received)
            if received >= total:
                self.progress.setVisible(False)

    # =====================
    # Bookmarks
    # =====================            

    def load_bookmarks(self):
        if os.path.exists(BOOKMARKS_FILE):
            with open(BOOKMARKS_FILE, "r") as f:
                self.bookmarks = json.load(f)
        else:
            self.bookmarks = []

    def save_bookmarks(self):
        with open(BOOKMARKS_FILE, "w") as f:
            json.dump(self.bookmarks, f)

    def add_bookmark(self):
        url = self.tabs.currentWidget().url().toString()
        title = self.tabs.currentWidget().page().title()
        if (title, url) not in self.bookmarks:
            self.bookmarks.append((title, url))
            self.save_bookmarks()
            QMessageBox.information(self, "Favorito", f"{title} adicionado aos favoritos!")

    def show_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Favoritos")
        layout = QVBoxLayout()
        list_widget = QListWidget()
        for title, url in reversed(self.bookmarks):
            list_widget.addItem(f"{title} - {url}")
        list_widget.itemDoubleClicked.connect(lambda item: self.open_bookmark(item))
        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.resize(600, 400)
        dialog.exec_()

    def open_bookmark(self, item):
        url = item.text().split(" - ")[-1]
        self.add_new_tab(url, "Nova Aba")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Gama Browser")
    window = MainWindow()
    sys.exit(app.exec_())
