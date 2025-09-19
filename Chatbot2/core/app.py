import os
from flask import Flask, render_template, request, jsonify
from chatbot import ChatBot
from servicos import Servicos
from relatorio import Relatorio, Relatorio_txt
from utils import Utils
from datetime import datetime

# Inicializa o aplicativo Flask
app = Flask(__name__, template_folder='templates')

# Define o caminho base do projeto
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')

# Inicializa as classes do chatbot e suas dependências
# O caminho para o arquivo de respostas é `data/respostasAleatorias.txt`
servicos = Servicos(os.path.join(data_dir, 'respostasAleatorias.txt'))
utils = Utils()
# A personalidade inicial é 'formal' para o servidor web
bot = ChatBot('formal', servicos)

# Inicializa os relatórios
Relatorio_txt().gerar()
Relatorio().Resetar_arquivo()

# Rota para a página inicial
@app.route('/')
def index():
    """Renderiza a página HTML principal do chatbot."""
    return render_template('index.html')

# Rota para lidar com as mensagens do chat
@app.route('/chat', methods=['POST'])
def chat():
    """Processa a mensagem do usuário e retorna a resposta do chatbot."""
    data = request.json
    pergunta = data.get('pergunta')
    persona_selecionada = data.get('persona', 'formal')

    if not pergunta:
        return jsonify({'resposta': 'Por favor, digite uma mensagem.'})

    bot.mudar_personalidade(persona_selecionada)
    resposta = bot.responder(pergunta)

    return jsonify({'resposta': resposta})

# Rota para gerar e retornar o relatório
@app.route('/relatorio')
def relatorio():
    """Gera o relatório completo e retorna seu conteúdo."""
    # Ações para gerar o relatório antes de retorná-lo
    Relatorio_txt.integrar_contadores()
    Relatorio().gerar()
    
    report_file_path = os.path.join(script_dir, 'relatorio.txt')
    try:
        with open(report_file_path, 'r', encoding='utf-8') as f:
            relatorio_conteudo = f.read()
    except FileNotFoundError:
        relatorio_conteudo = 'O arquivo de relatório não foi encontrado.'
    
    return jsonify({'relatorio': relatorio_conteudo})

# Executa o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
