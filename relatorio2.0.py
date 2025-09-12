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
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Falha ao instalar dependências.")
        sys.exit(1)


class Servicos:
    def __init__(self, arquivo="respostasAleatorias.txt"):
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


class Relatorio:
    def __init__(self, arquivo_csv="log_interacoes.csv"):
        self.arquivo_csv = arquivo_csv

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
        print("Interações por persona:")
        print(df["persona"].value_counts(), "\n")

        print("Top 5 perguntas:")
        print(df["pergunta_texto"].value_counts().head(5), "\n")

        fora_do_script = df[df["pergunta_numero"] == "N/A"]
        print(f"Perguntas fora do script: {len(fora_do_script)}")

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

    while True:
        pergunta = input("\nDigite sua dúvida (ou 'mudar' para trocar personalidade, 'historico' para ver, 'sair' para encerrar): ").strip().lower()
        if pergunta == "sair":
            Relatorio().gerar()
            print("Encerrando. Até logo!")
            break
        elif pergunta == "mudar":
            nova = escolher_personalidade()
            bot.mudar_personalidade(nova)
        elif pergunta == "historico":
            bot.exibir_historico()
        else:
            resposta = bot.responder(pergunta)
            print(f"[{bot.personalidade.capitalize()}] {resposta}")


if __name__ == "__main__":
    main()
# Fim do código
