import os
import sys
import subprocess
import random
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate


def instalar_dependencias():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError:
        print("Falha ao instalar as dependências.")
        sys.exit(1)


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
                    responder = respostas.get(self.estilo, "Não sei responder isso ainda.").split(" | ", 2)
        if responder:
            return random.choice(responder)
        return "Desculpe, não entendi sua pergunta."


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
    @staticmethod
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

        if 'persona' in df.columns and not df['persona'].empty:
            print("Interações por persona:")
            print(df['persona'].value_counts(), "\n")

        if 'pergunta_texto' in df.columns and not df['pergunta_texto'].empty:
            print("Perguntas mais frequentes:")
            print(df['pergunta_texto'].value_counts().head(10), "\n")

        fora_do_script = df[df['pergunta_numero'] == 'N/A']
        print(f"Perguntas fora do script: {len(fora_do_script)}")
        if not fora_do_script.empty:
            print(tabulate(
                fora_do_script[['data_hora', 'persona', 'pergunta_texto']],
                headers='keys', tablefmt='grid', showindex=False))

        if 'hora' in df.columns and not df['hora'].empty:
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

import os
import sys
import subprocess
import random
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate


# Função para instalar automaticamente as dependências listadas no requirements.txt
def instalar_dependencias():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependências instaladas com sucesso.")
    except subprocess.CalledProcessError:
        print("Falha ao instalar as dependências.")
        sys.exit(1)


# Classe que gerencia o carregamento das respostas do arquivo
class Servicos:
    def __init__(self, arquivo="respostas.txt"):
        self.dados = self.carregar_respostas_txt(arquivo)

    # Carrega as respostas categorizadas por chave e personalidade
    def carregar_respostas_txt(self, arquivo):
        respostas = {}
        categoria = None

        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                # Identifica nova categoria no arquivo
                if linha.startswith("[") and linha.endswith("]"):
                    categoria = linha[1:-1].lower()
                    respostas[categoria] = {}
                else:
                    # Divide a linha em chave, personalidade e resposta
                    chave, personalidade, resposta = linha.split(" | ", 2)
                    chave = chave.strip().lower()
                    personalidade = personalidade.strip().lower()

                    if chave not in respostas[categoria]:
                        respostas[categoria][chave] = {}

                    respostas[categoria][chave][personalidade] = resposta
        return respostas


# Classe que representa a personalidade do bot
class Personalidade:
    def __init__(self, estilo):
        self.estilo = estilo.lower()

    # Gera resposta baseada na chave da pergunta e na personalidade ativa
    def gerar_resposta(self, pergunta, servicos):
        responder = []
        pergunta = pergunta.lower()
        for categoria, intents in servicos.items():
            for chave, respostas in intents.items():
                if chave in pergunta:
                    responder = respostas.get(self.estilo, "Não sei responder isso ainda.").split(" | ", 2)
        if responder:
            return random.choice(responder)
        return "Desculpe, não entendi sua pergunta."


# Classe para armazenar e exibir o histórico da conversa
class Historico:
    def __init__(self):
        self.mensagens = []

    def adicionar(self, entrada, resposta):
        self.mensagens.append((entrada, resposta))

    def exibir(self):
        for i, (entrada, resposta) in enumerate(self.mensagens, 1):
            print(f"{i}. Usuário: {entrada}\n   Bot: {resposta}")

    # Cria ou sobrescreve o arquivo de histórico
    def criar_historico(self, arquivo=os.path.join(os.path.dirname(__file__), 'historico.txt')):
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n")
        with open(arquivo, "a+", encoding="utf-8") as f:
            for i, (entrada, resposta) in enumerate(self.mensagens, 1):
                f.write(f"{i}. Usuário: {entrada}\n   Bot: {resposta}\n")


# Classe responsável por registrar perguntas que o bot não soube responder
class Sugestoes:
    @staticmethod
    def adicionar_sugestao(pergunta):
        with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
            f.write(f"Sugestão de pergunta: {pergunta}\n")


# Classe principal do chatbot
class ChatBot:
    def __init__(self, personalidade, servicos):
        self.personalidade = Personalidade(personalidade)
        self.historico = Historico()
        self.servicos = servicos

    # Gera resposta e registra no histórico
    def responder(self, pergunta):
        resposta = self.personalidade.gerar_resposta(pergunta, self.servicos.dados)
        self.historico.adicionar(pergunta, resposta)
        return resposta

    # Permite trocar a personalidade durante a conversa
    def mudar_personalidade(self, nova_personalidade):
        self.personalidade = Personalidade(nova_personalidade)


# Classe para geração de relatórios e gráficos com base no log de interações
class Relatorio:
    def __init__(self, arquivo_csv='log_interacoes.csv'):
        self.arquivo_csv = arquivo_csv

    def gerar(self):
        print("\n===== RELATÓRIO DE USO DO CHATBOT =====\n")

        # Cria o arquivo se ele ainda não existir
        if not os.path.exists(self.arquivo_csv):
            print(f"Arquivo '{self.arquivo_csv}' não encontrado. Criando novo arquivo de log...")
            with open(self.arquivo_csv, mode='w', newline='', encoding='latin1') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['data_hora', 'persona', 'pergunta_numero', 'pergunta_texto'])
            print("Arquivo criado com sucesso, mas ainda não há dados para gerar o relatório.")
            return

        # Lê o arquivo CSV e trata erros
        try:
            df = pd.read_csv(self.arquivo_csv, encoding='latin1', delimiter=';')
        except pd.errors.ParserError:
            print("Erro ao ler o arquivo CSV. Verifique se o arquivo está no formato correto.")
            return

        # Verifica se o cabeçalho está correto
        colunas_esperadas = ['data_hora', 'persona', 'pergunta_numero', 'pergunta_texto']
        if not all(col in df.columns for col in colunas_esperadas):
            print("Erro: Cabeçalho não encontrado no arquivo CSV.")
            print(f"Colunas encontradas: {list(df.columns)}")
            return

        # Processa os dados
        df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
        df.dropna(subset=['data_hora'], inplace=True)
        df['dia'] = df['data_hora'].dt.date
        df['hora'] = df['data_hora'].dt.hour

        print(f"Total de interações registradas: {len(df)}\n")

        # Exibe estatísticas
        if 'persona' in df.columns and not df['persona'].empty:
            print("Interações por persona:")
            print(df['persona'].value_counts(), "\n")

        if 'pergunta_texto' in df.columns and not df['pergunta_texto'].empty:
            print("Perguntas mais frequentes:")
            print(df['pergunta_texto'].value_counts().head(10), "\n")

        # Filtra perguntas não reconhecidas
        fora_do_script = df[df['pergunta_numero'] == 'N/A']
        print(f"Perguntas fora do script: {len(fora_do_script)}")
        if not fora_do_script.empty:
            print(tabulate(
                fora_do_script[['data_hora', 'persona', 'pergunta_texto']],
                headers='keys', tablefmt='grid', showindex=False))

        # Exibe horário de pico
        if 'hora' in df.columns and not df['hora'].empty:
            hora_pico = df['hora'].value_counts().idxmax()
            print(f"\nHorário de pico: {hora_pico}:00 horas\n")

        # Gera gráficos a partir dos dados
        self.gerar_graficos(df)

        # Pergunta ao usuário se deseja abrir o arquivo no Excel
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

    # Gera e salva gráficos de análise de dados
    def gerar_graficos(self, df):
        try:
            if 'persona' in df.columns:
                plt.figure(figsize=(6, 4))
                df['persona'].value_counts().plot(kind='bar', color='skyblue')
                plt.title('Interações por Persona')
                plt.xlabel('Persona')
                plt.ylabel('Quantidade')
                plt.tight_layout()
                plt.savefig('grafico_persona.png')
                plt.close()

            if 'pergunta_texto' in df.columns:
                plt.figure(figsize=(8, 4))
                df['pergunta_texto'].value_counts().head(5).plot(kind='barh', color='orange')
                plt.title('Top 5 Perguntas Frequentes')
                plt.xlabel('Quantidade')
                plt.ylabel('Pergunta')
                plt.tight_layout()
                plt.savefig('grafico_perguntas.png')
                plt.close()

            if 'hora' in df.columns:
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


def escolher_personalidade():
    print("\n--- Escolha a personalidade ---")
    print("1 - Sr.Bot (formal)")
    print("2 - Clara (engraçada)")
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


def main():
    print("--- Bem-vindo ao ChatBot Banco X ---")
    print("Serviços: Pix, Cartão, Conta, Empréstimo")

    servicos = Servicos(os.path.join(os.path.dirname(__file__), 'respostas.txt'))
    personalidade_inicial = escolher_personalidade()
    bot = ChatBot(personalidade_inicial, servicos)

    try:
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "x+", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n")
    except FileExistsError:
        mensagem_a = []
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "r", encoding="utf-8") as file:
            hist = file.readlines()
            for i in range(len(hist) if len(hist) < 10 else 10):
                mensagem_a.append(hist[-(i+1)].strip())
        mensagem_a = "\n".join(reversed(mensagem_a))

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
            Sugestoes.adicionar_sugestao(pergunta)


if __name__ == "__main__":
    instalar_dependencias()
    main()
