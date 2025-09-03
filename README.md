# Gama Browser

Gama Browser é um navegador web construído em **Python** usando **PyQt5**.  
O projeto é voltado para aprendizado e implementação de funcionalidades básicas e intermediárias de um navegador moderno.

---

## Funcionalidades

### ✅ Fase 1 – Fundamentos
- **Abas múltiplas**: abrir, fechar, arrastar e alternar entre abas.
- **Barra de navegação**: Voltar, Avançar, Recarregar, Home, Nova Aba.
- **Barra de URL**: permite digitar e navegar para qualquer site.
- **Histórico de navegação**: visualizar páginas visitadas e abrir em nova aba.
- **Downloads simples**: salvar arquivos com diálogo de escolha de local e barra de progresso.

### ✅ Fase 2 – Funcionalidades avançadas básicas
- **Atalhos de teclado**:
  - `Ctrl+T` → Nova aba
  - `Ctrl+W` → Fechar aba
  - `Ctrl+Tab` / `Ctrl+Shift+Tab` → Alternar entre abas
- **Favoritos persistentes**:
  - Adicionar páginas aos favoritos.
  - Visualizar e abrir favoritos em nova aba.
  - Favoritos salvos em arquivo JSON para persistência entre sessões.
- **Tema escuro / claro**:
  - Alternar entre tema claro e escuro para o navegador.
- **Pesquisa rápida na barra de URL**:
  - `g termo` → pesquisa no Google
  - `w termo` → pesquisa na Wikipedia
  - `d termo` → pesquisa no DuckDuckGo
  - Pesquisa sem prefixo navega para a URL digitada (autocomplete `https://`).

---

## Requisitos

- Python 3.10+  
- PyQt5  
- PyQtWebEngine  

---

## Instalação das dependências via pip:

pip install PyQt5 PyQtWebEngine

---

## Como executar

python main.py

* O navegador abre com uma aba inicial apontando para o Google.

* Utilize a barra de URL, a barra de navegação ou os atalhos de teclado para explorar as funcionalidades.

---

## Observações

* O projeto é modular e pode ser expandido para incluir Fase 3 e 4, como modo leitura, downloads avançados, histórico avançado, bloqueio de anúncios, restauração de sessão, entre outros.

* Funciona melhor dentro de um venv no Linux (especialmente no Arch Linux) para evitar problemas com bibliotecas do PyQt5.

---

## Autor

Feito por **Luan Santos**