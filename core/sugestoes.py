import os

class Sugestoes:
    @staticmethod
    def adicionar_sugestao(pergunta):
        with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
            f.write(f"Sugestão de pergunta: {pergunta}\n")
