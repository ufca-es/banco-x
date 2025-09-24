import os
from datetime import datetime

class Sugestoes:
    def __init__(self, arquivo="sugestoes.txt"):
        self.arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), arquivo)

    def criar_arquivo(self):
        # Este método cria ou limpa o arquivo para uma nova sessão
        with open(self.arquivo, "w", encoding="utf-8") as f:
            f.write("Sugestões de Perguntas (sessão atual):\n")

    def adicionar_sugestao(self, pergunta):
        with open(self.arquivo, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {pergunta}\n")
