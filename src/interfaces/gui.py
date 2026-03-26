import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import BibliotecaDB
from logger import log
from datetime import datetime

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minha Biblioteca Pessoal v0.2")
        self.root.geometry("850x700")
        self.db = BibliotecaDB()

        # Configura um tema mais moderno do Tkinter
        estilo = ttk.Style()
        if 'clam' in estilo.theme_names():
            estilo.theme_use('clam')

        self._construir_interface()
        self._atualizar_lista()

    def _construir_interface(self):
        # ==========================================
        # 1. FRAME DE BUSCA (TOPO)
        # ==========================================
        frame_busca = ttk.Frame(self.root, padding=10)
        frame_busca.pack(fill=tk.X)

        ttk.Label(frame_busca, text="🔍 Buscar Livro:").pack(side=tk.LEFT, padx=5)
        self.entry_busca = ttk.Entry(frame_busca, width=40)
        self.entry_busca.pack(side=tk.LEFT, padx=5)
        self.entry_busca.bind("<KeyRelease>", self.realizar_busca)

        # ==========================================
        # 2. FRAME DE ENTRADA DE DADOS (FORMULÁRIO)
        # ==========================================
        frame_input = ttk.LabelFrame(self.root, text=" Adicionar Novo Livro ", padding=10)
        frame_input.pack(pady=5, padx=10, fill=tk.X)

        ttk.Label(frame_input, text="Título*:").grid(row=0, column=0, sticky="e", pady=2)
        self.entry_titulo = ttk.Entry(frame_input, width=40)
        self.entry_titulo.grid(row=0, column=1, columnspan=3, sticky="w", pady=2)

        ttk.Label(frame_input, text="Autor:").grid(row=1, column=0, sticky="e", pady=2)
        self.entry_autor = ttk.Entry(frame_input, width=40)
        self.entry_autor.grid(row=1, column=1, columnspan=3, sticky="w", pady=2)

        ttk.Label(frame_input, text="Páginas:").grid(row=2, column=0, sticky="e", pady=2)
        self.entry_paginas = ttk.Entry(frame_input, width=10)
        self.entry_paginas.grid(row=2, column=1, sticky="w", pady=2)

        ttk.Label(frame_input, text="Nota (0-10):").grid(row=2, column=2, sticky="e", pady=2)
        self.entry_nota = ttk.Entry(frame_input, width=10)
        self.entry_nota.grid(row=2, column=3, sticky="w", pady=2)

        ttk.Label(frame_input, text="Descrição:").grid(row=3, column=0, sticky="ne", pady=2)
        self.text_descricao = scrolledtext.ScrolledText(frame_input, width=45, height=3)
        self.text_descricao.grid(row=3, column=1, columnspan=3, pady=2)

        # Status
        self.var_status = tk.StringVar(value="Wishlist")
        frame_status = ttk.Frame(frame_input)
        frame_status.grid(row=4, column=1, columnspan=3, sticky="w", pady=5)
        ttk.Radiobutton(frame_status, text="Lido", variable=self.var_status, value="Lido").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame_status, text="Wishlist", variable=self.var_status, value="Wishlist").pack(side=tk.LEFT, padx=10)

        ttk.Button(frame_input, text="➕ Adicionar Livro", command=self.adicionar).grid(row=5, column=1, pady=10)

        # ==========================================
        # 3. FRAME DE LISTAGEM (ABAS E TABELAS)
        # ==========================================
        self.abas = ttk.Notebook(self.root)
        self.abas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.aba_wishlist = ttk.Frame(self.abas)
        self.aba_lidos = ttk.Frame(self.abas)

        self.abas.add(self.aba_wishlist, text="📚 Wishlist")
        self.abas.add(self.aba_lidos, text="✅ Lidos")

        # Configurando as Tabelas (Treeviews)
        colunas = ("Título", "Autor", "Páginas", "Nota", "Data de Adição")
        
        # Tabela Wishlist
        self.tree_wish = ttk.Treeview(self.aba_wishlist, columns=colunas, show="headings")
        self._configurar_tabela(self.tree_wish)
        self.tree_wish.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tabela Lidos
        self.tree_lidos = ttk.Treeview(self.aba_lidos, columns=colunas, show="headings")
        self._configurar_tabela(self.tree_lidos)
        self.tree_lidos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ==========================================
        # 4. FRAME DE AÇÕES (RODAPÉ)
        # ==========================================
        frame_acoes = ttk.Frame(self.root)
        frame_acoes.pack(pady=10)
        
        ttk.Button(frame_acoes, text="📄 Ver Detalhes / Editar", command=self.ver_detalhes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_acoes, text="🔄 Alternar Status", command=self.alternar_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_acoes, text="🗑️ Apagar Selecionado", command=self.deletar).pack(side=tk.LEFT, padx=5)

    def _configurar_tabela(self, tree):        
        tree.heading("Título", text="Título", command=lambda: self.ordenar_coluna(tree, "Título", False))
        tree.column("Título", width=300)
        
        tree.heading("Autor", text="Autor", command=lambda: self.ordenar_coluna(tree, "Autor", False))
        tree.column("Autor", width=200, anchor=tk.CENTER)

        tree.heading("Nota", text="Nota", command=lambda: self.ordenar_coluna(tree, "Nota", False))
        tree.column("Nota", width=50, anchor=tk.CENTER)

        tree.heading("Páginas", text="Páginas", command=lambda: self.ordenar_coluna(tree, "Páginas", False))
        tree.column("Páginas", width=50, anchor=tk.CENTER)

        tree.heading("Data de Adição", text="Data de Adição", command=lambda: self.ordenar_coluna(tree, "Data de Adição", False))
        tree.column("Data de Adição", width=120, anchor=tk.CENTER)

    # --- FUNÇÕES DE LÓGICA ---

    def _obter_selecao(self):
        aba_atual = self.abas.index(self.abas.select())
        tree_ativa = self.tree_wish if aba_atual == 0 else self.tree_lidos
        
        selecao = tree_ativa.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um livro na lista primeiro.")
            return None
        
        item = tree_ativa.item(selecao[0])
        return item['values'][-1] # O ID oculto é sempre o último valor da tupla

    def realizar_busca(self, event):
        termo = self.entry_busca.get().lower()
        self._atualizar_lista(filtro=termo)

    def adicionar(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get() or "Desconhecido"
        descricao = self.text_descricao.get("1.0", tk.END).strip()
        status = self.var_status.get()
        
        try:
            paginas = int(self.entry_paginas.get()) if self.entry_paginas.get() else 0
            nota = float(self.entry_nota.get()) if self.entry_nota.get() else 0.0
        except ValueError:
            messagebox.showerror("Erro", "Páginas (Inteiro) e Nota (ex: 8.5) precisam ser números.")
            return

        if titulo.strip():
            if self.db.adicionar_livro(titulo, autor, paginas, descricao, nota, status):
                self._limpar_campos()
                self._atualizar_lista()
                messagebox.showinfo("Sucesso", "Livro adicionado!")
        else:
            messagebox.showwarning("Aviso", "O título é obrigatório.")

    def deletar(self):
        livro_id = self._obter_selecao()
        if livro_id is None: return

        livro = self.db.obter_detalhes(livro_id)
        titulo = livro[1] 

        if messagebox.askyesno("Confirmar", f"Apagar {titulo}?"):
            if self.db.deletar_livro(livro_id):
                self._atualizar_lista()

    def alternar_status(self):
        livro_id = self._obter_selecao()
        if livro_id is None: return
        
        livro = self.db.obter_detalhes(livro_id)
        if livro:
            status_atual = livro[6] 
            novo_status = "Lido" if status_atual == "Wishlist" else "Wishlist"
            
            if self.db.atualizar_status(livro_id, novo_status):
                self._atualizar_lista()
                log.info(f"Status alternado via GUI para: {novo_status}")

    def ver_detalhes(self):
        livro_id = self._obter_selecao()
        if livro_id is None: return

        livro = self.db.obter_detalhes(livro_id)
        if livro:
            janela = tk.Toplevel(self.root)
            janela.title(f"Detalhes: {livro[1]}")
            janela.geometry("500x350")
            
            frame_input_edicao = ttk.LabelFrame(janela, text=" Ver detalhes ", padding=10)
            frame_input_edicao.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

            ttk.Label(frame_input_edicao, text="Título*:").grid(row=0, column=0, sticky="e", pady=2)
            self.entry_titulo_detalhes = ttk.Entry(frame_input_edicao, width=55)
            self.entry_titulo_detalhes.grid(row=0, column=1, columnspan=3, sticky="w", pady=2)
            self.entry_titulo_detalhes.insert(0, livro[1])
            self.entry_titulo_detalhes.config(state='disabled')

            ttk.Label(frame_input_edicao, text="Autor:").grid(row=1, column=0, sticky="e", pady=2)
            self.entry_autor_detalhes = ttk.Entry(frame_input_edicao, width=55)
            self.entry_autor_detalhes.grid(row=1, column=1, columnspan=3, sticky="w", pady=2)
            self.entry_autor_detalhes.insert(0, livro[2])
            self.entry_autor_detalhes.config(state='disabled')

            ttk.Label(frame_input_edicao, text="Páginas:").grid(row=2, column=0, sticky="e", pady=2)
            self.entry_paginas_detalhes = ttk.Entry(frame_input_edicao, width=10)
            self.entry_paginas_detalhes.grid(row=2, column=1, sticky="w", pady=2)
            self.entry_paginas_detalhes.insert(0, livro[3])
            self.entry_paginas_detalhes.config(state='disabled')

            ttk.Label(frame_input_edicao, text="Nota (0-10):").grid(row=2, column=2, sticky="e", pady=2)
            self.entry_nota_detalhes = ttk.Entry(frame_input_edicao, width=10)
            self.entry_nota_detalhes.grid(row=2, column=3, sticky="w", pady=2)
            self.entry_nota_detalhes.insert(0, livro[5])
            self.entry_nota_detalhes.config(state='disabled')

            ttk.Label(frame_input_edicao, text="Descrição:").grid(row=3, column=0, sticky="ne", pady=2)
            self.text_descricao_detalhes = scrolledtext.ScrolledText(frame_input_edicao, width=45, height=6)
            self.text_descricao_detalhes.grid(row=3, column=1, columnspan=3, pady=2)
            self.text_descricao_detalhes.insert(tk.INSERT, livro[4])
            self.text_descricao_detalhes.config(state=tk.DISABLED)

            def habilitar_edicao():
                self.entry_titulo_detalhes.config(state='normal')
                self.entry_autor_detalhes.config(state='normal')
                self.entry_paginas_detalhes.config(state='normal')
                self.entry_nota_detalhes.config(state='normal')
                self.text_descricao_detalhes.config(state=tk.NORMAL) 
                btn_acao.config(text="Salvar Alterações", command=salvar_edicao)

            def salvar_edicao():
                try:
                    novo_titulo = self.entry_titulo_detalhes.get()
                    novo_autor = self.entry_autor_detalhes.get()
                    novas_paginas = int(self.entry_paginas_detalhes.get())
                    nova_nota = float(self.entry_nota_detalhes.get())
                    nova_descricao = self.text_descricao_detalhes.get("1.0", tk.END).strip()

                    if self.db.atualizar_livro(livro_id, novo_titulo, novo_autor, novas_paginas, nova_descricao, nova_nota):
                        
                        self.entry_titulo_detalhes.config(state='disabled')
                        self.entry_autor_detalhes.config(state='disabled')
                        self.entry_paginas_detalhes.config(state='disabled')
                        self.entry_nota_detalhes.config(state='disabled')
                        self.text_descricao_detalhes.config(state=tk.DISABLED)

                        btn_acao.config(text="Editar Informações", command=habilitar_edicao)
                        self._atualizar_lista()
                        # messagebox.showinfo("Sucesso", "Informações atualizadas!")
                except ValueError:
                    messagebox.showerror("Erro", "Páginas precisa ser um número inteiro e Nota um número com ponto.")

            btn_acao = ttk.Button(janela, text="Editar Informações", command=habilitar_edicao)
            btn_acao.pack(pady=10)

    def ordenar_coluna(self, tree, col, reverse):
        """Ordena o conteúdo do Treeview ao clicar no cabeçalho da coluna."""
        lista_valores = [(tree.set(k, col), k) for k in tree.get_children('')]
        
        lista_valores.sort(reverse=reverse)

        for index, (val, k) in enumerate(lista_valores):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: self.ordenar_coluna(tree, col, not reverse))

    def _limpar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_paginas.delete(0, tk.END)
        self.entry_nota.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        self.entry_busca.delete(0, tk.END)

    def _atualizar_lista(self, filtro=""):
        for item in self.tree_wish.get_children(): self.tree_wish.delete(item)
        for item in self.tree_lidos.get_children(): self.tree_lidos.delete(item)

        livros = self.db.listar_livros()
        
        for livro in livros:
            livro_id = livro[0]
            titulo = livro[1]
            autor = livro[2]
            paginas = livro[3]
            data_banco = livro[4] 
            status = livro[5]
            nota = livro[6]

            try:
                data_string = str(data_banco).split(" ")[0] 
                data_obj = datetime.strptime(data_string, "%Y-%m-%d")
                data_formatada = data_obj.strftime("%d/%m/%Y")
            except Exception:
                data_formatada = "Desconhecida"

            if filtro and filtro not in titulo.lower() and filtro not in autor.lower():
                continue

            # A tupla com os exatos 4 valores visíveis + o ID oculto no final
            valores = (titulo, autor, paginas, nota, data_formatada, livro_id)  

            if status == "Lido":
                self.tree_lidos.insert('', tk.END, values=valores)
            else:
                self.tree_wish.insert('', tk.END, values=valores)

    def on_closing(self):
        self.db.fechar_conexao()
        self.root.destroy()