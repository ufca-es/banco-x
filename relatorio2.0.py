pip install -r requirements.txt

import os
import random
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import subprocess
import tabulate

class Servicos:
    def __init__(self, arquivo="respostas.txt"):
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
                    # Formato: chave | personalidade | resposta
                    chave, personalidade, resposta = linha.split(" | ", 2)
                    chave = chave.strip().lower()
                    personalidade = personalidade.strip().lower()

                    if chave not in respostas[categoria]:
                        respostas[categoria][chave] = {}

                    respostas[categoria][chave][personalidade] = resposta
        return respostas


class Personalidade:
    def __init__(self, estilo):
        self.estilo = estilo.lower()

    def gerar_resposta(self, pergunta, servicos):
        responder = []
        pergunta = pergunta.lower()
        for categoria, intents in servicos.items():
            for chave, respostas in intents.items():
                if chave in pergunta:
                    #transforma o dicionário em lista e divide em cada " | "
                    responder = respostas.get(self.estilo, "Não sei responder isso ainda.").split(" | ", 2) 
        if responder:
            # Se houver múltiplas respostas, escolhe uma aleatoriamente, se não, retorna a resposta padrão ou a mensagem de não saber responder
            return random.choice(responder) 
        return "Desculpe, não entendi sua pergunta."

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

class ChatBot:
    def __init__(self, personalidade, servicos):
        self.personalidade = Personalidade(personalidade)
        self.historico = Historico()
        self.servicos = servicos

    def responder(self, pergunta):
        resposta = self.personalidade.gerar_resposta(pergunta, self.servicos.dados)
        self.historico.adicionar(pergunta, resposta)
        return resposta

    def mudar_personalidade(self, nova_personalidade):
        self.personalidade = Personalidade(nova_personalidade)

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
                print(tabulate(
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

# O usuario digita so escolhe o numero indicado pra mudar de personalidade
def escolher_personalidade():
    print("\n--- Escolha a personalidade ---")
    print("1 - Sr.Bot (formal)")
    print("2 - Clara (engracada)")
    print("3 - Byte (rude)")
    print("4 - Marcos (empreendedor)")
    opcao = input("Digite o número: ").strip()
    mapa = {
        "1": "formal",
        "2": "engracada",
        "3": "rude",
        "4": "empreendedor"
    }
    return mapa.get(opcao, "formal")

# Introdução do Bot
def main():
    print("--- Bem-vindo ao ChatBot Banco X ---")
    print("Serviços: Pix, Cartão, Conta, Empréstimo")

    servicos = Servicos(os.path.join(os.path.dirname(__file__), 'respostas.txt'))
    personalidade_inicial = escolher_personalidade()
    bot = ChatBot(personalidade_inicial, servicos)

    try:
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "x+", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n") # Cria o arquivo de historico se não existir
    except FileExistsError: # Se o arquivo já existir, lê as 5 últimas mensagens do histórico
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
        pergunta = input("\nDigite sua dúvida (ou 'mudar' para trocar personalidade, 'historico' para ver, 'sair' para encerrar): ").lower()

        if pergunta == "sair":
            print("Encerrando atendimento. Até logo!")
            bot.historico.criar_historico()
            Relatorio().gerar()
            break
        elif pergunta == "mudar":
            nova = escolher_personalidade()
            bot.mudar_personalidade(nova)
            continue
        elif pergunta == "historico":
            bot.historico.exibir()
            continue

        resposta = bot.responder(pergunta)
        print(f"[{bot.personalidade.estilo.capitalize()}] {resposta}")
        if resposta == "Desculpe, não entendi sua pergunta.":
            Sugestoes.adicionar_sugestao(pergunta) # Adiciona a sugestão ao arquivo de sugestões de perguntas
           

if __name__ == "__main__":
    main()
