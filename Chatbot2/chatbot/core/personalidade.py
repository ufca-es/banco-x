import random

class Personalidade:
    def __init__(self, estilo):
        self.estilo = estilo.lower()

    def gerar_resposta(self, pergunta, servicos):
        respostas = []
        pergunta = pergunta.lower()
        for categoria, intents in servicos.items():
            for chave, opcoes in intents.items():
                if chave in pergunta:
                    if isinstance(opcoes, dict):
                        lista_respostas = opcoes.get(self.estilo, [])
                        if isinstance(lista_respostas, list):
                            respostas.extend(lista_respostas)
                        else:
                            respostas.append(lista_respostas)
        if respostas:
            return random.choice(respostas)
        return "Desculpe, não entendi sua pergunta."
