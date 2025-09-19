import os
from flask import Flask, render_template, request, jsonify
from core.chatbot import ChatBot
from core.servicos import Servicos
from core.relatorio import Relatorio, Relatorio_txt
from core.sugestoes import Sugestoes
from core.personalidade import Personalidade

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Configuração de caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESPOSTAS_FILE = os.path.join(DATA_DIR, 'respostasAleatorias.txt')

# Inicializa as classes do chatbot
servicos = Servicos(RESPOSTAS_FILE)
# A personalidade inicial pode ser definida aqui, ou você pode deixar o chatbot escolher
chatbot = ChatBot(personalidade=Personalidade('formal'), servicos=servicos)

# Inicia o relatório no começo do aplicativo
Relatorio().Resetar_arquivo()
Relatorio_txt().gerar()
Sugestoes().criar_arquivo()

# Rota principal para a página do chatbot
@app.route('/')
def home():
    """
    Renderiza a página inicial do chatbot (index.html).
    """
    return render_template('index.html')

# Rota para lidar com as interações do chat
@app.route('/chat', methods=['POST'])
def chat():
    """
    Recebe a mensagem do usuário via POST e retorna a resposta do chatbot em JSON.
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "Por favor, digite uma mensagem."}), 400

    response = chatbot.responder(user_message)
    return jsonify({"response": response})

# Rota para mudar a personalidade do chatbot
@app.route('/change_persona', methods=['POST'])
def change_persona():
    """
    Muda a personalidade do chatbot com base na entrada do usuário.
    """
    new_persona = request.json.get('persona')
    if not new_persona:
        return jsonify({"response": "Personalidade inválida."}), 400

    chatbot.mudar_personalidade(new_persona)
    return jsonify({"response": f"Minha personalidade agora é {new_persona}."})

# Rota para gerar e exibir o relatório
@app.route('/get_report', methods=['GET'])
def get_report():
    """
    Gera o relatório de interações e retorna o conteúdo do arquivo.
    """
    Relatorio_txt().integrar_contadores()
    report_content = Relatorio().gerar()
    return jsonify({"report": report_content})

# Rota para o histórico
@app.route('/get_historico', methods=['GET'])
def get_historico():
    """
    Retorna o histórico de conversas em formato JSON.
    """
    history_content = chatbot.historico.mensagens
    return jsonify({"historico": history_content})

# Rota para salvar o histórico em um arquivo
@app.route('/save_historico', methods=['POST'])
def save_historico():
    """
    Salva o histórico de conversas em um arquivo de texto.
    """
    chatbot.historico.criar_historico()
    return jsonify({"status": "Histórico salvo com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
