import os
import sys
import subprocess
from historico import Historico
from relatorio import Relatorio
from relatorio import Relatorio_txt
from servicos import Servicos
from chatbot import ChatBot
from sugestoes import Sugestoes
from utils import Utils


def main():
    print("--- Bem-vindo ao ChatBot Banco X ---")
    print("Serviços: Pix, Cartão, Conta, Empréstimo")

    # Inicializa utilidades e dependências
    utils = Utils()
    personalidade_inicial = utils.escolher_personalidade()
    # Carrega serviços e personalidade inicial
    servicos = Servicos(os.path.join(os.path.dirname(__file__), '..', 'data', 'respostasAleatorias.txt'))

    bot = ChatBot(personalidade_inicial, servicos)

    # Arquivo histórico
    try:
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "x+", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n")
    except FileExistsError:
        pass

    Relatorio_txt().gerar()
    Relatorio().Resetar_arquivo()
    # Arquivo sugestões
    with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
        f.write("\nSugestões de Perguntas da sessão passada:\n")

    while True:
        pergunta = input("\nDigite sua dúvida (ou 'mudar', 'historico', 'sair'): ").lower()

        if pergunta == "sair":
            print("Encerrando atendimento. Até logo!")
            bot.historico.criar_historico()
            Relatorio_txt().integrar_contadores()
            Relatorio().gerar()
            break
        elif pergunta == "mudar":
            nova = utils.escolher_personalidade()
            bot.mudar_personalidade(nova)
            continue
        elif pergunta == "historico":
            bot.exibir_historico()
            continue

        resposta = bot.responder(pergunta)
        print(f"[{bot.personalidade.capitalize()}] {resposta}")
        Relatorio_txt.contadores_personas(bot.personalidade)
        if resposta == "Desculpe, não entendi sua pergunta.":
            Sugestoes().adicionar_sugestao(pergunta)

if __name__ == "__main__":
    main()
