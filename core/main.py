import os
from servicos import Servicos
from chatbot import ChatBot
from sugestoes import Sugestoes
from relatorio import Relatorio
from utils import escolher_personalidade

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
    main()
