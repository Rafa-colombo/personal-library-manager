import argparse
from database import BibliotecaDB
from logger import log

def rodar_cli():
    parser = argparse.ArgumentParser(description="Gerenciador de Biblioteca Pessoal CLI")
    
    # Ações principais
    parser.add_argument('--add', type=str, help="Adicionar um novo livro (Requer título)")
    parser.add_argument('--listar', action='store_true', help="Listar todos os livros")
    parser.add_argument('--deletar', type=int, help="Deletar um livro pelo ID", metavar="ID")
    parser.add_argument('--detalhes', type=int, help="Ver detalhes de um livro pelo ID", metavar="ID")
    
    # Metadados opcionais para adição
    parser.add_argument('--autor', type=str, default="Desconhecido", help="Autor do livro")
    parser.add_argument('--paginas', type=int, default=0, help="Número de páginas")
    parser.add_argument('--descricao', type=str, metavar='TXT', default="", help="Breve descrição ou resenha")
    parser.add_argument('--nota', type=float, default=0.0, help="Sua nota pessoal (ex: 4.5)")
    parser.add_argument('--status', type=str, choices=['Lido', 'Wishlist'], default='Wishlist', help="Status do livro")
    parser.add_argument('--atualizar', type=int, help="Atualizar o status de um livro pelo ID", metavar="ID")

    args = parser.parse_args()
    db = BibliotecaDB()

    if args.add:
        print(f"Adicionando '{args.add}'...")
        if db.adicionar_livro(args.add, args.autor, args.paginas, args.descricao, args.nota, args.status):
            print("Adicionado com sucesso!")
        else:
            print("Erro ao adicionar. Verifique os logs.")
            
    elif args.listar:
        livros = db.listar_livros()
        print("\n--- Sua Biblioteca ---")
        for livro in livros:
            print(f"[ID: {livro[0]}] {livro[1]} (por {livro[2]}) - {livro[3]}")
        print("----------------------\n")
        
    elif args.deletar:
        if db.deletar_livro(args.deletar):
            print(f"Livro ID {args.deletar} removido da biblioteca.")
        else:
            print(f"Livro ID {args.deletar} não encontrado.")
            
    elif args.detalhes:
        livro = db.obter_detalhes(args.detalhes)
        if livro:
            print("\n--- Detalhes do Livro ---")
            print(f"ID: {livro[0]}\nTítulo: {livro[1]}\nAutor: {livro[2]}")
            print(f"Páginas: {livro[3]}\nNota: {livro[5]}/10.0\nStatus: {livro[6]}")
            print(f"Adicionado em: {livro[7]}")
            print(f"Descrição: {livro[4]}")
            print("-------------------------\n")
        else:
            print(f"Livro ID {args.detalhes} não encontrado.")
            
    elif args.atualizar:
        print(f"Atualizando o status do livro ID {args.atualizar} para '{args.status}'...")
        if db.atualizar_status(args.atualizar, args.status):
            print("Status atualizado com sucesso!")
        else:
            print("Erro: Livro não encontrado ou falha na atualização.")
            
    else:
        parser.print_help()

    db.fechar_conexao()