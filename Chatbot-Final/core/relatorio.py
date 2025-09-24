import os
import pandas as pd
import csv
import matplotlib.pyplot as plt
from tabulate import tabulate

class Relatorio:
    def Resetar_arquivo(self):
        if os.path.exists(self.arquivo_csv):
            with open(self.arquivo_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["data_hora", "persona", "pergunta_numero", "pergunta_texto"])

    def __init__(self, arquivo_csv=None):
        # Caminho absoluto para garantir que o arquivo seja encontrado
        if arquivo_csv is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.arquivo_csv = os.path.join(script_dir, "log_interacoes.csv")
        else:
            self.arquivo_csv = arquivo_csv

    def gerar(self):
        print("\n===== RELATÓRIO DE USO DO CHATBOT =====\n")

        if not os.path.exists(self.arquivo_csv):
            print(f"Arquivo '{self.arquivo_csv}' não encontrado.")
            return

        # Lê o CSV
        try:
            df = pd.read_csv(self.arquivo_csv, encoding="utf-8", sep=";")
        except Exception as e:
            print(f"Erro ao ler CSV: {e}")
            return

        if df.empty:
            print("Nenhuma interação registrada.")
            return

        # Converte datas
        df["data_hora"] = pd.to_datetime(df["data_hora"], errors="coerce")
        df.dropna(subset=["data_hora"], inplace=True)
        df["hora"] = df["data_hora"].dt.hour

        # Estatísticas
        print(f"Total de interações: {len(df)}\n")
        print("Interações por persona:")
        print(df["persona"].value_counts(), "\n")

        print("Top 5 perguntas:")
        print(df["pergunta_texto"].value_counts().head(5), "\n")

        # Perguntas fora do script
        fora_do_script = df[df["pergunta_numero"] == "N/A"]
        print(f"Perguntas fora do script: {len(fora_do_script)}")

        if not fora_do_script.empty:
            print(tabulate(
                fora_do_script[["data_hora", "persona", "pergunta_texto"]],
                headers="keys", tablefmt="grid", showindex=False
            ))

        self.gerar_graficos(df)

    def gerar_graficos(self, df):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Gráfico 1: Interações por persona
            df["persona"].value_counts().plot(kind="bar", title="Interações por Persona")
            plt.tight_layout()
            plt.savefig(os.path.join(script_dir, "grafico_persona.png"))
            Relatorio_txt.integrar_personas(df["persona"].nunique())
            plt.close()

            # Gráfico 2: Top 5 perguntas
            df["pergunta_texto"].value_counts().head(5).plot(
                kind="barh", title="Top 5 Perguntas Frequentes", color="orange"
            )
            plt.tight_layout()
            plt.savefig(os.path.join(script_dir, "grafico_perguntas.png"))
            Relatorio_txt.integrar_top5perguntas(", ".join(df["pergunta_texto"].value_counts().head(5).index))
            plt.close()

            # Gráfico 3: Interações por hora
            df["hora"].value_counts().sort_index().plot(kind="bar", title="Interações por Hora")
            plt.tight_layout()
            plt.savefig(os.path.join(script_dir, "grafico_hora.png"))
            Relatorio_txt.integrar_Ninterações(len(df))
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
