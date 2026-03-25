import logging

# Configuração do logger

def setup_logger():
    # Cria e configura o logger
    logger = logging.getLogger("BibliotecaApp")
    logger.setLevel(logging.INFO)

    # Evita adicionar múltiplos handlers se a função for chamada várias vezes
    if not logger.handlers:
        # Salva em arquivo
        file_handler = logging.FileHandler("historico_app.log", encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s] - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Instância global para ser importada pelos outros módulos
log = setup_logger()