# 📚 Minha Biblioteca Pessoal (Personal Library Manager)

Um gerenciador de biblioteca pessoal leve, rápido e de código aberto. Cadastre seus livros, gerencie sua lista de desejos (Wishlist), dê notas e acompanhe suas leituras de forma organizada.

🚀 **100% Nativo & Independente:** Este projeto foi construído **exclusivamente com a Standard Library do Python**. Nenhuma biblioteca externa (`pip install`) é necessária para rodar a aplicação. Além disso, pode ser compilado em um único arquivo executável (`.exe`) para rodar em qualquer máquina sem precisar ter o Python instalado.

---

## ✨ Funcionalidades

* **Gerenciamento Completo (CRUD):** Adicione, visualize, atualize o status e apague livros da sua coleção.
* **Interface Gráfica Moderna:** Construída com `tkinter` e o módulo `ttk` (Themed Tkinter), com separação limpa por abas nativas.
* **Busca em Tempo Real:** Filtre sua lista de livros instantaneamente enquanto digita o título ou o autor.
* **Banco de Dados Local Seguro:** Utiliza `sqlite3` para salvar todas as informações em um arquivo leve e invisível para o controle de versão.
* **Sistema de Logs:** Registro automático de todas as ações e erros em um arquivo `historico_app.log` para fácil auditoria.
* **Portabilidade:** Empacotado via PyInstaller, permitindo levar o executável e o banco de dados em um pen drive para qualquer computador.

---

## 🛠️ Arquitetura e Tecnologias

A aplicação segue uma arquitetura modular inspirada no padrão MVC, separando a interface lógica do acesso aos dados:

* **Linguagem:** Python 3.x
* **GUI:** `tkinter` & `tkinter.ttk`
* **Banco de Dados:** `sqlite3`
* **Logging:** `logging` (Standard Library)
* **Build/Empacotamento:** `pyinstaller` (Apenas para geração do executável)

---

## 🚀 Como Usar

Você tem duas formas de utilizar este projeto: rodando o executável final ou executando direto do código-fonte.

### Opção 1: Versão Portátil (Usuário Final)
Se você possui o arquivo `MinhaBiblioteca.exe`:
1. Coloque o executável em uma pasta de sua preferência.
2. Dê um duplo clique.
3. *Nota:* Na primeira execução, o sistema criará automaticamente os arquivos `biblioteca.db` (seu banco de dados) e `historico_app.log` na mesma pasta. Mantenha-os juntos para não perder seus dados.

### Opção 2: Rodando do Código-Fonte (Desenvolvedores)
Como o projeto não possui dependências externas, o setup é imediato:

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SeuUsuario/seu-repositorio.git](https://github.com/SeuUsuario/seu-repositorio.git)
