import os
import pandas as pd
import matplotlib.pyplot as plt
import tabulate

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
            script_dir = os.path.dirname(os.path.abspath(__file__))
            plt.savefig(os.path.join(script_dir, "grafico_persona.png"))
            plt.close()

            df["pergunta_texto"].value_counts().head(5).plot(kind="barh", title="Top 5 Perguntas Frequentes", color="orange")
            plt.tight_layout()
            plt.savefig(os.path.join(script_dir, "grafico_perguntas.png"))
            plt.close()

            df["hora"].value_counts().sort_index().plot(kind="bar", title="Interações por Hora")
            plt.tight_layout()
            plt.savefig(os.path.join(script_dir, "grafico_hora.png"))
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
