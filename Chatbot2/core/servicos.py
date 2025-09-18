import os

class Servicos:
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'respostasAleatorias.txt')  
    def __init__(self, arquivo=file_path):
        self.arquivo = arquivo
        self.dados = self.carregar_respostas_txt()

    def carregar_respostas_txt(self):
        respostas = {}
        categoria = None

        with open(self.arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                if linha.startswith("[") and linha.endswith("]"):
                    categoria = linha[1:-1].lower()
                    respostas[categoria] = {}
                else:
                    chave, personalidade, resposta = linha.split(" | ", 2)
                    chave = chave.strip().lower()
                    personalidade = personalidade.strip().lower()
                    resposta = resposta.strip()

                    if chave not in respostas[categoria]:
                        respostas[categoria][chave] = {}

                    if personalidade not in respostas[categoria][chave]:
                        respostas[categoria][chave][personalidade] = []

                    respostas[categoria][chave][personalidade].append(resposta)
        return respostas
