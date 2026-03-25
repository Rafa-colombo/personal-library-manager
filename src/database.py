import sqlite3
from logger import log

class BibliotecaDB:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabelas()
        log.info(f"Conexão estabelecida com o banco: {db_name}")

    def _criar_tabelas(self):
        # Tabela atualizada com os novos campos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT,
                paginas INTEGER,
                descricao TEXT,
                nota REAL,
                status TEXT NOT NULL CHECK(status IN ('Lido', 'Wishlist')),
                data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def adicionar_livro(self, titulo, autor, paginas, descricao, nota, status):
        try:
            query = '''INSERT INTO livros (titulo, autor, paginas, descricao, nota, status) 
                       VALUES (?, ?, ?, ?, ?, ?)'''
            self.cursor.execute(query, (titulo, autor, paginas, descricao, nota, status))
            self.conn.commit()
            log.info(f"Livro adicionado: '{titulo}' na categoria '{status}'.")
            return True
        except Exception as e:
            log.error(f"Erro ao adicionar livro '{titulo}': {e}")
            return False

    def deletar_livro(self, livro_id):
        try:
            self.cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                log.info(f"Livro ID {livro_id} deletado com sucesso.")
                return True
            return False
        except Exception as e:
            log.error(f"Erro ao deletar livro ID {livro_id}: {e}")
            return False

    def obter_detalhes(self, livro_id):
        self.cursor.execute("SELECT * FROM livros WHERE id = ?", (livro_id,))
        return self.cursor.fetchone()

    def listar_livros(self):
        # Trazendo o autor junto para a listagem básica
        self.cursor.execute("SELECT id, titulo, autor, status, data_adicao FROM livros")
        return self.cursor.fetchall()

    def atualizar_status(self, livro_id: int, novo_status: str):
        try:
            # O UPDATE do SQL muda apenas o campo status onde o ID for igual ao informado
            self.cursor.execute("UPDATE livros SET status = ? WHERE id = ?", (novo_status, livro_id))
            self.conn.commit()
            
            # Verifica se alguma linha foi realmente alterada (se o ID existe)
            if self.cursor.rowcount > 0:
                log.info(f"Status do livro ID {livro_id} atualizado para '{novo_status}'.")
                return True
            return False
        except Exception as e:
            log.error(f"Erro ao atualizar status do livro ID {livro_id}: {e}")
            return False

    def fechar_conexao(self):
        self.conn.close()
        log.info("Conexão com o banco encerrada.")