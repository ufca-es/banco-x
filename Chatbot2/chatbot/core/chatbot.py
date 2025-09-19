import os
import csv
import random
from datetime import datetime
from .personalidade import Personalidade
from .historico import Historico

class ChatBot:
    def __init__(self, personalidade, servicos):
        self.personalidade = personalidade
        self.servicos = servicos
        self.historico = Historico()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(script_dir, "log_interacoes.csv")

    def responder(self, pergunta):
        pergunta = pergunta.lower()
        encontrou = False
        for categoria, chaves in self.servicos.dados.items():
            for chave, estilos in chaves.items():
                if chave in pergunta:
                    respostas = estilos.get(self.personalidade.estilo, [])
                    if respostas:
                        resposta = random.choice(respostas)
                        self.registrar_interacao(pergunta, chave)
                        self.historico.adicionar(pergunta, resposta)
                        return resposta
                    encontrou = True
        if not encontrou:
            self.registrar_interacao(pergunta, "N/A")
        return "Desculpe, não entendi sua pergunta."

    def registrar_interacao(self, pergunta, chave):
        with open(self.log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            if f.tell() == 0:
                writer.writerow(["data_hora", "persona", "pergunta_numero", "pergunta_texto"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.personalidade.estilo, chave, pergunta])

    def mudar_personalidade(self, nova_personalidade):
        self.personalidade = Personalidade(nova_personalidade)
        
    def exibir_historico(self):
        if not self.historico.mensagens:
            print("Não há histórico de mensagens.")
            return
        
        for i, (pergunta, resposta) in enumerate(self.historico.mensagens, 1):
            print(f"{i}. Usuário: {pergunta}")
            print(f"   Bot: {resposta}")
