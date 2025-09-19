import os
# Sem mudanças
class Historico:
    def __init__(self):
        self.mensagens = []

    def adicionar(self, entrada, resposta):
        self.mensagens.append((entrada, resposta))

    def exibir(self):
        for i, (entrada, resposta) in enumerate(self.mensagens, 1):
            print(f"{i}. Usuário: {entrada}\n   Bot: {resposta}")

    def criar_historico(self, arquivo=os.path.join(os.path.dirname(__file__), 'historico.txt')):
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n")
        with open(arquivo, "a+", encoding="utf-8") as f:
            for i, (entrada, resposta) in enumerate(self.mensagens, 1):
                f.write(f"{i}. Usuário: {entrada}\n   Bot: {resposta}\n")

