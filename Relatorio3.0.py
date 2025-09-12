import os
import sys
import csv
import subprocess
import random
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate


# Instala dependências
def instalar_dependencias():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
    except subprocess.CalledProcessError:
        print("Falha ao instalar dependências.")
        sys.exit(1)


class Servicos:
    file_path = os.path.join(os.path.dirname(__file__), "respostasAleatorias.txt")  
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


class ChatBot:
    def __init__(self, personalidade, servicos):
        self.personalidade = personalidade
        self.servicos = servicos
        self.historico = []
        self.log_file = "log_interacoes.csv"

    def responder(self, pergunta):
        pergunta = pergunta.lower()
        encontrou = False
        for categoria, chaves in self.servicos.dados.items():
            for chave, estilos in chaves.items():
                if chave in pergunta:
                    respostas = estilos.get(self.personalidade, [])
                    if respostas:
                        resposta = random.choice(respostas)
                        self.registrar_interacao(pergunta, chave)
                        self.historico.append((pergunta, resposta))
                        return resposta
                    encontrou = True
        if not encontrou:
            self.registrar_interacao(pergunta, "N/A")
            self.registrar_sugestao(pergunta)
        return "Desculpe, não entendi sua pergunta."

    def registrar_interacao(self, pergunta, chave):
        with open(self.log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            if f.tell() == 0:
                writer.writerow(["data_hora", "persona", "pergunta_numero", "pergunta_texto"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.personalidade, chave, pergunta])

    def registrar_sugestao(self, pergunta):
        with open("sugestoes.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {pergunta}\n")

    def mudar_personalidade(self, nova_personalidade):
        self.personalidade = nova_personalidade

    def exibir_historico(self):
        for i, (entrada, resposta) in enumerate(self.historico, 1):
            print(f"{i}. Você: {entrada}")
            print(f"   Bot ({self.personalidade}): {resposta}")


# Aqui é um histórico básico, ele não salva em arquivo txt, ele serve apenas para implementar as classes, fazer mudanças futuras
# L: Agora ele salva o histórico em um arquivo txt, mas reescreve com o novo histórico sempre que o programa é encerrado
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


class Sugestoes:
     def adicionar_sugestao(pergunta):
        with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
            f.write(f"Sugestão de pergunta: {pergunta}\n")

class Relatorio:
    def __init__(self, arquivo_csv="log_interacoes.csv"):
        self.arquivo_csv = arquivo_csv

    def Resetar_arquivo(self):
        if os.path.exists(self.arquivo_csv):
            with open(self.arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["data_hora", "persona", "pergunta_numero", "pergunta_texto"])

    def gerar(self):
        print("\n===== RELATÓRIO DE USO DO CHATBOT =====\n")
        if not os.path.exists(self.arquivo_csv):
            print(f"Arquivo '{self.arquivo_csv}' não encontrado.")
            return

        df = pd.read_csv(self.arquivo_csv, encoding="utf-8", delimiter=";")
        if df.empty:
            print("Nenhuma interação registrada.")
            return

        df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
        df.dropna(subset=["data_hora"], inplace=True)
        df["hora"] = df["data_hora"].dt.hour

        print(f"Total de interações: {len(df)}\n")
        Relatorio_txt.integrar_Ninterações(len(df))
        print("Interações por persona:")
        print(df["persona"].value_counts(), "\n")
        Relatorio_txt.integrar_personas(df["persona"].nunique())

        print("Top 5 perguntas:")
        print(df["pergunta_texto"].value_counts().head(5), "\n")

        fora_do_script = df[df["pergunta_numero"] == "N/A"]
        print(f"Perguntas fora do script: {len(fora_do_script)}")
       
        Relatorio_txt.integrar_top5perguntas(df["pergunta_texto"].value_counts().head(5).to_dict())

        if not fora_do_script.empty:
            print(tabulate(fora_do_script[["data_hora", "persona", "pergunta_texto"]],
                           headers="keys", tablefmt="grid", showindex=False))

        self.gerar_graficos(df)

    def gerar_graficos(self, df):
        try:
            df["persona"].value_counts().plot(kind="bar", title="Interações por Persona")
            plt.tight_layout()
            plt.savefig("grafico_persona.png")
            plt.close()

            df["pergunta_texto"].value_counts().head(5).plot(kind="barh", title="Top 5 Perguntas Frequentes", color="orange")
            plt.tight_layout()
            plt.savefig("grafico_perguntas.png")
            plt.close()

            df["hora"].value_counts().sort_index().plot(kind="bar", title="Interações por Hora")
            plt.tight_layout()
            plt.savefig("grafico_hora.png")
            plt.close()

            print("Gráficos gerados com sucesso.")
        except Exception as e:
            print(f"Erro ao gerar gráficos: {e}")

class Relatorio_txt:
    contador = [0, 0, 0, 0]  # Contador para cada persona: [formal, engraçada, rude, empreendedor]
    def gerar(self):
        arquivo = os.path.join(os.path.dirname(__file__), 'relatorio.txt')
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write("Relatório de Interações do ChatBot\n\n")
    def integrar_personas(personas):
        arquivo = os.path.join(os.path.dirname(__file__), 'relatorio.txt')
        with open(arquivo, "a+", encoding="utf-8") as f:
            f.write(f"Personas utilizadas: {personas}\n")
    def integrar_Ninterações(interacoes):
        arquivo = os.path.join(os.path.dirname(__file__), 'relatorio.txt')
        with open(arquivo, "a+", encoding="utf-8") as f:
            f.write(f"Total de interações: {interacoes}\n")
    def integrar_top5perguntas(perguntas):
        arquivo = os.path.join(os.path.dirname(__file__), 'relatorio.txt')
        with open(arquivo, "a+", encoding="utf-8") as f:
            f.write(f"Top 5 perguntas:{perguntas}\n")
    def contadores_personas(persona_ativa):
        for i, persona in enumerate(["formal", "engracada", "rude", "empreendedor"]):
            if persona == persona_ativa:
                Relatorio_txt.contador[i] += 1
    def integrar_contadores(self):
        arquivo = os.path.join(os.path.dirname(__file__), 'relatorio.txt')
        with open(arquivo, "a+", encoding="utf-8") as f:
            f.write(f"Uso de cada persona:\nSrBot {self.contador[0]}\nClara {self.contador[1]}\nByte {self.contador[2]}\nMarcos {self.contador[3]}\n")

def escolher_personalidade():
    print("\n--- Escolha a personalidade ---")
    print("1 - Sr.Bot (formal)")
    print("2 - Clara (engraçada)")
    print("3 - Byte (rude)")
    print("4 - Marcos (empreendedor)")
    opcao = input("Digite o número: ").strip()
    return {
        "1": "formal",
        "2": "engracada",
        "3": "rude",
        "4": "empreendedor"
    }.get(opcao, "formal")


def main():
    instalar_dependencias()
    servicos = Servicos()
    personalidade = escolher_personalidade()
    bot = ChatBot(personalidade, servicos)
    Relatorio_txt().gerar()
    Relatorio().Resetar_arquivo()
    
    try:
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "x+", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n") # Cria o arquivo de historico se não existir
    except FileExistsError: 
        # Isso não faz nada além de pegar as ultimas 5 mensagens da última conversa e armazenar numa lista, foi uma task passada. NÃO DELETAR
        mensagem_a = []
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "r", encoding="utf-8") as file:
            hist = file.readlines()
            for i in range(len(hist) if len(hist) < 10 else 10):
                mensagem_a.append(hist[-(i+1)].strip())
        mensagem_a = "\n".join(reversed(mensagem_a))

    # Separa o histórico de sugestões da conversa acontecendo da passada.
    with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
        f.write("\nSugestões de Perguntas da sessão passada:\n")

    while True:
        pergunta = input("\nDigite sua dúvida (ou 'mudar' para trocar personalidade, 'historico' para ver, 'sair' para encerrar): ").strip().lower()
        if pergunta == "sair":
            Relatorio().gerar()
            Relatorio_txt().integrar_contadores()
            print("Encerrando. Até logo!")
            Historico().criar_historico()
            break
        elif pergunta == "mudar":
            nova = escolher_personalidade()
            bot.mudar_personalidade(nova)
        elif pergunta == "historico":
            bot.exibir_historico()
        else:
            resposta = bot.responder(pergunta)
            print(f"[{bot.personalidade.capitalize()}] {resposta}")
            Relatorio_txt.contadores_personas(bot.personalidade) # Conta o uso de cada persona
            if resposta == "Desculpe, não entendi sua pergunta.":
                Sugestoes.adicionar_sugestao(pergunta) # Adiciona a sugestão ao arquivo de sugestões de perguntas TASK PASSADA


if __name__ == "__main__":
    main()
# Fim do código
