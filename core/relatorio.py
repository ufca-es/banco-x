import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import tabulate

class Relatorio:
    def __init__(self, arquivo_csv='log_interacoes.csv'):
        self.arquivo_csv = arquivo_csv

    def gerar(self):
        print("\n===== RELATÓRIO DE USO DO CHATBOT =====\n")
        
        if not os.path.exists(self.arquivo_csv):
            print(f"Arquivo '{self.arquivo_csv}' não encontrado. Criando novo arquivo de log...")
            with open(self.arquivo_csv, mode='w', newline='', encoding='latin1') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['data_hora', 'persona', 'pergunta_numero', 'pergunta_texto'])
            print("Arquivo criado com sucesso, mas ainda não há dados para gerar o relatório.")
            return

        try:
            df = pd.read_csv(self.arquivo_csv, encoding='latin1', delimiter=';')
        except pd.errors.ParserError:
            print("Erro ao ler o arquivo CSV. Verifique se o arquivo está no formato correto.")
            return

        colunas_esperadas = ['data_hora', 'persona', 'pergunta_numero', 'pergunta_texto']
        if not all(col in df.columns for col in colunas_esperadas):
            print("Erro: Cabeçalho não encontrado no arquivo CSV.")
            print(f"Colunas encontradas: {list(df.columns)}")
            return

        df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
        df.dropna(subset=['data_hora'], inplace=True)
        df['dia'] = df['data_hora'].dt.date
        df['hora'] = df['data_hora'].dt.hour

        print(f"Total de interações registradas: {len(df)}\n")

        print("Interações por persona:")
        print(df['persona'].value_counts(), "\n")

        print("Perguntas mais frequentes:")
        print(df['pergunta_texto'].value_counts().head(10), "\n")

        fora_do_script = df[df['pergunta_numero'] == 'N/A']
        print(f"Perguntas fora do script: {len(fora_do_script)}")
        if not fora_do_script.empty:
            if tabulate:
                print(tabulate.tabulate(
                    fora_do_script[['data_hora', 'persona', 'pergunta_texto']],
                    headers='keys', tablefmt='grid', showindex=False))
            else:
                print(fora_do_script[['data_hora', 'persona', 'pergunta_texto']].to_string(index=False))

        if not df['hora'].empty:
            hora_pico = df['hora'].value_counts().idxmax()
            print(f"\nHorário de pico: {hora_pico}:00 horas\n")

        self.gerar_graficos(df)

        while True:
            abrir_excel = input("\nDeseja abrir o arquivo de relatório (log_interacoes.csv) no Excel? (s/n): ").strip().lower()
            if abrir_excel == 's':
                try:
                    os.startfile(self.arquivo_csv)
                except Exception as e:
                    print(f"Não foi possível abrir o Excel automaticamente: {e}")
                break
            elif abrir_excel == 'n':
                break
            else:
                print("Digite 's' para sim ou 'n' para não.")

    def gerar_graficos(self, df):
        try:
            plt.figure(figsize=(6, 4))
            df['persona'].value_counts().plot(kind='bar', color='skyblue')
            plt.title('Interações por Persona')
            plt.xlabel('Persona')
            plt.ylabel('Quantidade')
            plt.tight_layout()
            plt.savefig('grafico_persona.png')
            plt.close()

            plt.figure(figsize=(8, 4))
            df['pergunta_texto'].value_counts().head(5).plot(kind='barh', color='orange')
            plt.title('Top 5 Perguntas Frequentes')
            plt.xlabel('Quantidade')
            plt.ylabel('Pergunta')
            plt.tight_layout()
            plt.savefig('grafico_perguntas.png')
            plt.close()

            plt.figure(figsize=(8, 4))
            df['hora'].value_counts().sort_index().plot(kind='bar', color='green')
            plt.title('Interações por Hora do Dia')
            plt.xlabel('Hora')
            plt.ylabel('Quantidade')
            plt.tight_layout()
            plt.savefig('grafico_hora.png')
            plt.close()

            print("Gráficos salvos como:")
            print(" - grafico_persona.png")
            print(" - grafico_perguntas.png")
            print(" - grafico_hora.png")
        except Exception as e:
            print(f"Erro ao gerar gráficos: {e}")
