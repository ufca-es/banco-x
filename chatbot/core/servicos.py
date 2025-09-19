import os

class Servicos:
    # Define o caminho do arquivo de dados para o novo formato TXT
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'possiveisPerguntas.txt')
    
    def __init__(self, arquivo=file_path):
        self.arquivo = arquivo
        self.dados = self.carregar_respostas_txt()

    def carregar_respostas_txt(self):
        """
        Carrega as respostas de um arquivo de texto.
        O formato do arquivo é:
        [categoria]
        chave | personalidade | resposta
        """
        respostas = {}
        categoria_atual = None

        with open(self.arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                if linha.startswith("[") and linha.endswith("]"):
                    # Se for uma linha de categoria, atualiza a categoria atual
                    categoria_atual = linha[1:-1].lower()
                    if categoria_atual not in respostas:
                        respostas[categoria_atual] = {}
                elif categoria_atual:
                    try:
                        # Separa a linha em chave, personalidade e resposta
                        partes = linha.split(" | ", 2)
                        chave = partes[0].strip().lower()
                        personalidade = partes[1].strip().lower()
                        resposta = partes[2].strip()

                        if chave not in respostas[categoria_atual]:
                            respostas[categoria_atual][chave] = {}

                        if personalidade not in respostas[categoria_atual][chave]:
                            respostas[categoria_atual][chave][personalidade] = []

                        respostas[categoria_atual][chave][personalidade].append(resposta)
                    except (IndexError, ValueError) as e:
                        print(f"Erro ao processar a linha: '{linha}' no arquivo {self.arquivo}. Erro: {e}")
        return respostas
