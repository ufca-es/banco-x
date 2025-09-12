import os

class Servicos:
    def __init__(self, arquivo="respostas.txt"):
        
        # Deixa eu ver se isso resolve o problema de não encontrar os arquivos
        arquivo = Path(_file_).resolve().parent.parent / "dados" / "respostasAleatorias.txt"
        self.dados = self.carregar_respostas_txt(arquivo)

    def carregar_respostas_txt(self, arquivo):
        respostas = {}
        categoria = None

        with open(arquivo, "r", encoding="utf-8") as f:
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

                    if chave not in respostas[categoria]:
                        respostas[categoria][chave] = {}

                    respostas[categoria][chave][personalidade] = resposta
        return respostas



