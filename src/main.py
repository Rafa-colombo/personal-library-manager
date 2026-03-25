""" 
 Projeto de um sistema de gerenciamento de livros lidos e a ler, utilizando Python puro. 

Bibliotecas nativas: Sqlite3 para o banco de dados, datetime para manipulação de datas, logging para registro de atividades, t
kinter para a interface gráfica, os e sys para operações de sistema.

"""

import sys
from logger import log

def main():
    log.info("Aplicação iniciada.")
    
    # Se houver argumentos além do nome do script, roda a CLI
    if len(sys.argv) > 1:
        log.info("Modo CLI detectado.")
        from interfaces.cliUse import rodar_cli
        rodar_cli()
    else:
        # Se não houver argumentos, abre a interface gráfica
        log.info("Modo GUI detectado.")
        import tkinter as tk
        from interfaces.gui import AppGUI
        
        root = tk.Tk()
        app = AppGUI(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()

if __name__ == "__main__":
    main()