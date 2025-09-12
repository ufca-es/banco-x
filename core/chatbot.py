from personalidade import Personalidade
from historico import Historico

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
