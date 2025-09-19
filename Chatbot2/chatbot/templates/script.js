<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistente Financeiro</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* Estilos gerais do corpo da página */
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #f0f0f0;
            background: #0d0d0d;
        }

        /* Container do Chatbot com efeito de glassmorphism */
        .chatbot-container {
            width: 380px;
            height: 600px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
            transition: transform 0.3s ease-in-out;
        }

        /* Bolha de fundo decorativa */
        .chatbot-container::before {
            content: '';
            position: absolute;
            top: -50px;
            left: -50px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, #f97316 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(50px);
            opacity: 0.3;
            z-index: -1;
            animation: moveBubble1 15s infinite alternate ease-in-out;
        }

        .chatbot-container::after {
            content: '';
            position: absolute;
            bottom: -50px;
            right: -50px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, #ea580c 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(50px);
            opacity: 0.3;
            z-index: -1;
            animation: moveBubble2 18s infinite alternate ease-in-out;
        }

        @keyframes moveBubble1 {
            from { transform: translate(0, 0) scale(1); }
            to { transform: translate(50px, 50px) scale(1.1); }
        }

        @keyframes moveBubble2 {
            from { transform: translate(0, 0) scale(1); }
            to { transform: translate(-50px, -50px) scale(1.1); }
        }

        /* Telas do aplicativo */
        .screen {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .hidden {
            display: none;
        }

        /* Cabeçalho do Chatbot */
        .chatbot-header {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 15px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: #fff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .personalidade-display {
            display: flex;
            align-items: center;
            font-size: 0.9rem;
            font-weight: normal;
            gap: 10px;
        }

        .persona-btn {
            background-color: #f97316;
            color: #fff;
            border: none;
            padding: 8px 12px;
            border-radius: 15px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .persona-btn:hover {
            background-color: #ea580c;
        }

        /* Área de mensagens */
        .chat-messages {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            scrollbar-width: thin;
            scrollbar-color: #ea580c #1a1a1a;
        }

        /* Barra de rolagem customizada para Webkit (Chrome, Safari) */
        .chat-messages::-webkit-scrollbar {
            width: 8px;
        }

        .chat-messages::-webkit-scrollbar-track {
            background: transparent;
        }

        .chat-messages::-webkit-scrollbar-thumb {
            background-color: #ea580c;
            border-radius: 4px;
        }

        /* Estilo das mensagens */
        .message {
            max-width: 80%;
            padding: 12px 18px;
            border-radius: 20px;
            line-height: 1.5;
            word-wrap: break-word;
            font-size: 0.95rem;
        }

        /* Mensagens do usuário */
        .message.user {
            align-self: flex-end;
            background-color: #f97316;
            color: #fff;
            border-bottom-right-radius: 5px;
        }

        /* Mensagens do bot */
        .message.bot {
            align-self: flex-start;
            background-color: rgba(255, 255, 255, 0.1);
            color: #e5e5e5;
            border-bottom-left-radius: 5px;
        }

        /* Rodapé com a caixa de input */
        .chatbot-footer {
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Campo de texto */
        .chatbot-input {
            flex-grow: 1;
            padding: 12px 18px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }

        .chatbot-input::placeholder {
            color: #a0a0a0;
        }

        .chatbot-input:focus {
            border-color: #f97316;
            background-color: rgba(255, 255, 255, 0.15);
        }

        /* Botão de envio */
        .chatbot-send-btn {
            background-color: #ea580c;
            color: #fff;
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s, transform 0.2s;
        }

        .chatbot-send-btn:hover {
            background-color: #f97316;
            transform: scale(1.05);
        }

        .chatbot-send-btn svg {
            fill: #fff;
            width: 24px;
            height: 24px;
        }

        /* Estilos do Relatório */
        .report-content {
            flex-grow: 1;
            padding: 20px;
            color: #e5e5e5;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: #ea580c transparent;
        }

        .report-content h2 {
            color: #f97316;
            margin-top: 0;
            font-size: 1.5rem;
            border-bottom: 2px solid #f97316;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .report-content h3 {
            color: #fff;
            font-size: 1.2rem;
            margin-top: 25px;
            margin-bottom: 15px;
        }

        .report-content p, .report-content ul, .report-content pre {
            color: #c0c0c0;
        }

        .report-content ul {
            list-style-type: none;
            padding: 0;
        }

        .report-content li {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            border-left: 3px solid #f97316;
            font-size: 0.9rem;
        }

        .report-content li strong {
            color: #fff;
        }

        .report-content pre {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 15px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Estilos para o relatório */
        .report-item.user {
            color: #fff;
            font-weight: bold;
            background: none;
            border-left: none;
            margin-bottom: 5px;
        }

        .report-item.bot {
            color: #c0c0c0;
            font-style: italic;
            font-weight: normal;
            background: none;
            border-left: none;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

    <div class="chatbot-container">
        
        <div id="chat-screen" class="screen">
            <div class="chatbot-header">
                ChatBot
                <div class="personalidade-display">
                    <span id="persona-name">Sr. Bot</span>
                    <button id="change-persona-btn" class="persona-btn">Mudar</button>
                </div>
            </div>
            <div class="chat-messages">
                <!-- As mensagens serão inseridas aqui pelo JavaScript -->
            </div>
            <div class="chatbot-footer">
                <input type="text" id="chat-input" class="chatbot-input" placeholder="Digite sua mensagem...">
                <button id="send-btn" class="chatbot-send-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
        </div>

        <div id="report-screen" class="screen hidden">
            <div class="chatbot-header">
                Relatório de Interações
                <button id="back-to-chat-btn" class="persona-btn">Voltar</button>
            </div>
            <div id="report-content" class="report-content">
                <!-- O conteúdo do relatório será inserido aqui pelo JavaScript -->
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const chatInput = document.getElementById('chat-input');
            const sendBtn = document.getElementById('send-btn');
            const chatMessages = document.querySelector('.chat-messages');
            const chatScreen = document.getElementById('chat-screen');
            const reportScreen = document.getElementById('report-screen');
            const backToChatBtn = document.getElementById('back-to-chat-btn');
            const reportContent = document.getElementById('report-content');
        
            // Variáveis para a gestão de personalidade
            const personaNameDisplay = document.getElementById('persona-name');
            const changePersonaBtn = document.getElementById('change-persona-btn');
            const personas = ["Sr. Bot", "Dona Sol", "Byte", "Marcos"];
            const personalidades = ["formal", "engracada", "rude", "empreendedor"];
            let currentPersonaIndex = 0;
            
            // Histórico da conversa
            let historico = [];
        
            // Função para adicionar uma mensagem à conversa
            const addMessage = (sender, text) => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message', sender);
                messageDiv.textContent = text;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                historico.push({ sender, text });
            };
        
            // Função para enviar uma mensagem para o assistente
            const sendMessage = async () => {
                const text = chatInput.value.trim();
                if (text === '') return;
        
                addMessage('user', text);
                chatInput.value = '';
                
                // Exibe o relatório se a palavra-chave for "relatorio"
                if (text.toLowerCase() === 'relatorio') {
                    showReport('Exemplo de relatório do servidor. Este conteúdo seria gerado por um backend real.');
                    return;
                }
        
                const currentPersonality = personalidades[currentPersonaIndex];
        
                // Simulação da resposta do assistente.
                // Substitui a chamada de API por uma resposta local.
                addMessage('bot', `Simulando uma resposta do assistente com a personalidade "${currentPersonality}" para a sua mensagem: "${text}"`);
            };
        
            // Lida com o clique no botão e a tecla Enter
            sendBtn.addEventListener('click', sendMessage);
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        
            // Função para mostrar a tela de relatório
            const showReport = (reportText) => {
                chatScreen.classList.add('hidden');
                reportScreen.classList.remove('hidden');
        
                // Limpa o conteúdo e adiciona o relatório formatado
                reportContent.innerHTML = '';
                const reportTitle = document.createElement('h2');
                reportTitle.textContent = 'Relatório de Interações';
                reportContent.appendChild(reportTitle);
        
                const conversationHistoryTitle = document.createElement('h3');
                conversationHistoryTitle.textContent = 'Histórico da Conversa';
                reportContent.appendChild(conversationHistoryTitle);
        
                historico.forEach(item => {
                    const reportItem = document.createElement('div');
                    reportItem.classList.add('report-item', item.sender);
                    reportItem.textContent = `${item.sender.toUpperCase()}: ${item.text}`;
                    reportContent.appendChild(reportItem);
                });
        
                const backendReportTitle = document.createElement('h3');
                backendReportTitle.textContent = 'Relatório do Servidor (Simulado)';
                reportContent.appendChild(backendReportTitle);
        
                const preElement = document.createElement('pre');
                preElement.textContent = reportText;
                reportContent.appendChild(preElement);
            };
        
            // Volta para a tela de chat
            backToChatBtn.addEventListener('click', () => {
                reportScreen.classList.add('hidden');
                chatScreen.classList.remove('hidden');
            });
        
            // Alterna a personalidade do bot
            changePersonaBtn.addEventListener('click', () => {
                currentPersonaIndex = (currentPersonaIndex + 1) % personas.length;
                personaNameDisplay.textContent = personas[currentPersonaIndex];
                addMessage('bot', `Minha personalidade agora é ${personas[currentPersonaIndex]}.`);
            });
        
            // Mensagem inicial
            addMessage('bot', 'Olá! Eu sou o assistente financeiro do Banco-X. Como posso ajudar?');
        });
    </script>
</body>
</html>
