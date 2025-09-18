import os
import sys
import subprocess
from historico import Historico
from relatorio import Relatorio
from relatorio import Relatorio_txt
from servicos import Servicos
from chatbot import ChatBot
from sugestoes import Sugestoes
from relatorio import Relatorio
from utils import Utils

def instalar_dependencias():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
    except subprocess.CalledProcessError:
        print("Falha ao instalar dependências.")
        sys.exit(1)

def main():
    instalar_dependencias()
    servicos = Servicos()
    personalidade = Utils.escolher_personalidade()
    bot = ChatBot(personalidade, servicos)
    historico = Historico()  # instância usada no loop
    relatorio_txt = Relatorio_txt()
    relatorio_txt.gerar()
    relatorio = Relatorio()

    try:
        with open(os.path.join(os.path.dirname(__file__), 'historico.txt'), "x+", encoding="utf-8") as f:
            f.write("Histórico de Conversas:\n")
    except FileExistsError:
        pass  # já existe

    with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
        f.write("\nSugestões de Perguntas da sessão passada:\n")

    while True:
        pergunta = input("\nDigite sua dúvida (ou 'mudar' para trocar personalidade, 'historico' para ver, 'sair' para encerrar): ").strip().lower()
        if pergunta == "sair":
            relatorio.gerar()
            relatorio_txt.integrar_contadores()
            historico.criar_historico()
            print("Encerrando. Até logo!")
            print("\nArquivos gerados:")
            break
        elif pergunta == "mudar":
            nova = Utils.escolher_personalidade()
            bot.mudar_personalidade(nova)
        elif pergunta == "historico":
            bot.exibir_historico()
        else:
            resposta = bot.responder(pergunta)
            print(f"[{bot.personalidade}] {resposta}")
            historico.adicionar(pergunta, resposta)  # <-- adiciona ao histórico
            Relatorio_txt.contadores_personas(bot.personalidade)
            if resposta == "Desculpe, não entendi sua pergunta.":
                Sugestoes.adicionar_sugestao(pergunta)

    # Separa o histórico de sugestões da conversa acontecendo da passada.
    with open(os.path.join(os.path.dirname(__file__), 'sugestoes.txt'), "a+", encoding="utf-8") as f:
        f.write("\nSugestões de Perguntas da sessão passada:\n")

if __name__ == "__main__":
    main()
# Fim do código