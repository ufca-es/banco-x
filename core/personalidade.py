import random

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
