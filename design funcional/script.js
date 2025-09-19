document.addEventListener('DOMContentLoaded', () => {
    // 1. Referências aos elementos HTML
    const chatScreen = document.getElementById('chat-screen');
    const reportScreen = document.getElementById('report-screen');
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const personaNameDisplay = document.getElementById('persona-name');
    const changePersonaBtn = document.getElementById('change-persona-btn');
    const backToChatBtn = document.getElementById('back-to-chat-btn');
    const reportContent = document.getElementById('report-content');

    // 2. Dados e estado simulados
    const respostas = {
        pix: {
            formal: ["Para realizar uma transferência via Pix, acesse o menu ‘Pix’ no aplicativo, selecione a chave do destinatário, informe o valor e confirme a operação.", "A transação é processada instantaneamente.", "No aplicativo, vá em ‘Pix’, insira a chave, o valor e confirme.", "O valor cairá na hora."],
            engracada: ["É rapidinho! Abra o app, vai em ‘Pix’, digita a chave do amigo ou do boleto, coloca o valor e pronto :).", "Vai lá no app, clica em ‘Pix’, digita a chave e o valor e pá!", "Dinheiro voando.", "Abre o app, acha o ‘Pix’, coloca a chave e valor e tcham!", "Tá feito.", "Pix é tipo mágica: abre o app, chave, valor e pronto."],
            rude: ["Abra o app, vai em ‘Pix’, escolha a chave, coloque o valor e confirme.", "Vai no app, Pix, chave, valor. Pronto.", "Abre o app, coloca a chave no Pix, digita o valor e envia.", "App, Pix, chave, valor, confirma. Simples."],
            empreendedor: ["Ótimo! Para movimentar seu dinheiro rápido, abra o app, vá em ‘Pix’, escolha a chave do destinatário, digite o valor e confirme!", "No app, selecione ‘Pix’, digite a chave e valor, e tenha liquidez imediata.", "Use o Pix para otimizar sua gestão financeira: chave, valor e pronto.", "Em poucos cliques no app, com o Pix, transfira seu capital instantaneamente."]
        },
        cartao: {
            formal: ["Em caso de perda, bloqueie imediatamente seu cartão pelo aplicativo ou pelo telefone 0800 123 4567. Em seguida, solicite a emissão de um novo cartão.", "Caso tenha perdido o cartão, acesse o app ou ligue 0800 para bloqueio imediato.", "Se perder seu cartão, bloqueie pelo aplicativo ou telefone e peça um novo.", "Perda do cartão? Bloqueie pelo app ou 0800 e solicite substituição."],
            engracada: ["Eita! Primeiro bloqueia pelo app ou ligue para a gente, depois peça um novo.", "Ninguém quer que alguém use seu cartão sem permissão, não é?", "Ops! Perdeu o cartão? Corre no app, bloqueia e pede outro.", "Cartão sumiu? Bloqueia rápido no app e já pede um novo.", "Ih, perdeu o cartão? Melhor bloquear no app antes que ele vá passear sem você."],
            rude: ["Bloqueie no app ou liga no 0800. Peça outro cartão.", "Perdeu? Bloqueia logo no app e pede outro.", "App ou 0800, bloqueia e resolve.", "Cartão perdido? Bloqueia e solicita outro, simples."],
            empreendedor: ["Bloqueie imediatamente pelo app ou ligue para nós. Depois solicite um novo cartão para continuar tocando seus pagamentos sem atrasos.", "Para evitar prejuízos, bloqueie pelo app ou telefone e já peça a reposição.", "Mantenha o fluxo: bloqueie pelo app e solicite substituição do cartão.", "Garanta a segurança e a continuidade: bloqueie e substitua seu cartão."]
        },
        conta: {
            formal: ["As tarifas aplicáveis estão detalhadas na tabela de preços disponível em nosso site, na seção ‘Tarifas e Serviços’.", "Consulte a tabela de tarifas no site, na área ‘Tarifas e Serviços’.", "Todas as tarifas estão descritas no site oficial, seção ‘Tarifas e Serviços’.", "Verifique as tarifas no site, área ‘Serviços e Tarifas’."],
            engracada: ["Ninguém gosta de tarifas, não é? Mas elas ficam na seção ‘Tarifas e Serviços’, bem explicadinhas.", "Tarifas? Estão todas no site, e explicadas de um jeito fácil.", "As tarifas estão no site, mas olha, eu sei que ninguém curte elas.", "Confere no site a lista de tarifas, prometo que é rapidinho."],
            rude: ["Todas as tarifas estão no nosso site. Vai e confere.", "Quer saber tarifas? Site. Pronto.", "Tá no site. Não tem segredo.", "Olha no site e pronto."],
            empreendedor: ["Vamos otimizar seus custos: todas as tarifas estão detalhadas no site.", "Confira as tarifas no site para planejar melhor seu fluxo financeiro.", "Consulte as tarifas e otimize seu orçamento.", "Tenha controle: verifique as tarifas no site e ajuste sua estratégia."]
        },
        genericas: {
            saudacao: ["Olá! Sou seu assistente financeiro virtual. Em que posso ajudar?", "Oi! Como posso ser útil hoje?"],
            relatorio: "Com certeza. Preparei um relatório com base em nossas interações. Clique no botão 'Ver Relatório' para acessá-lo.",
            despedida: ["Até logo! Se precisar de algo, é só me chamar.", "Tchau! Tenha um ótimo dia."],
            desconhecida: ["Desculpe, não entendi. Você pode perguntar sobre 'Pix', 'cartão' ou 'tarifas'.", "Não consegui identificar sua pergunta. Tente algo como 'perdi meu cartão'."]
        }
    };
    
    // Controles de estado
    let currentPersona = 'formal';
    let chatHistory = [];
    let canSendMessage = false;

    // 3. Funções de manipulação do chat
    
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getBotResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        let key = "desconhecida";

        if (lowerMessage.includes('pix') || lowerMessage.includes('transferencia')) {
            key = 'pix';
        } else if (lowerMessage.includes('cartao') || lowerMessage.includes('perda') || lowerMessage.includes('roubo')) {
            key = 'cartao';
        } else if (lowerMessage.includes('tarifa') || lowerMessage.includes('custo') || lowerMessage.includes('servico')) {
            key = 'conta';
        } else if (lowerMessage.includes('relatorio')) {
            key = 'relatorio';
        } else if (lowerMessage.includes('tchau') || lowerMessage.includes('sair')) {
            key = 'despedida';
        } else if (lowerMessage.includes('ola') || lowerMessage.includes('oi') || lowerMessage.includes('bom dia')) {
            key = 'saudacao';
        }
        
        // Simula a lógica de resposta do seu código Python
        let response = '';
        if (key === 'relatorio') {
            response = respostas.genericas.relatorio;
            setTimeout(() => {
                showReport();
            }, 1000);
        } else if (key in respostas.genericas) {
            response = respostas.genericas[key][Math.floor(Math.random() * respostas.genericas[key].length)];
        } else {
            response = respostas[key][currentPersona][Math.floor(Math.random() * respostas[key][currentPersona].length)];
        }

        return response;
    }

    function sendMessage() {
        if (!canSendMessage) {
            return;
        }

        const userMessage = chatInput.value.trim();
        if (userMessage !== '') {
            appendMessage(userMessage, 'user');
            chatHistory.push({ user: userMessage, persona: currentPersona });
            chatInput.value = '';
            
            canSendMessage = false;
            
            const botResponse = getBotResponse(userMessage);

            setTimeout(() => {
                appendMessage(botResponse, 'bot');
                canSendMessage = true;
            }, 1000); // Atraso de 1 segundo para simular o processamento
        }
    }

    // 4. Funções de controle de tela e relatório
    
    function showReport() {
        chatScreen.classList.add('hidden');
        reportScreen.classList.remove('hidden');
        generateReportContent();
    }

    function hideReport() {
        chatScreen.classList.remove('hidden');
        reportScreen.classList.add('hidden');
    }

    function generateReportContent() {
        let reportHTML = '<h2>Visão Geral do Relatório</h2>';
        reportHTML += '<p>Baseado em suas interações nesta sessão.</p>';
        reportHTML += '<h3>Histórico de Mensagens:</h3><ul>';
        
        chatHistory.forEach((item, index) => {
            reportHTML += `<li><strong>#${index + 1}</strong>: "${item.user}" (Persona: ${item.persona.charAt(0).toUpperCase() + item.persona.slice(1)})</li>`;
        });
        reportHTML += '</ul>';

        // Simula dados estatísticos
        const totalMessages = chatHistory.length;
        const personaCounts = chatHistory.reduce((acc, item) => {
            acc[item.persona] = (acc[item.persona] || 0) + 1;
            return acc;
        }, {});

        reportHTML += '<h3>Estatísticas da Sessão:</h3>';
        reportHTML += `<p>Total de Mensagens: ${totalMessages}</p>`;
        reportHTML += '<p>Uso de Personalidades:</p>';
        reportHTML += '<pre>' + JSON.stringify(personaCounts, null, 2) + '</pre>';

        reportContent.innerHTML = reportHTML;
    }

    // 5. Funções para mudança de personalidade
    
    function changePersona() {
        const personas = ['formal', 'engracada', 'rude', 'empreendedor'];
        let newPersona = prompt(`Escolha uma personalidade:\n1 - Sr. Bot (Formal)\n2 - Clara (Engraçada)\n3 - Byte (Rude)\n4 - Marcos (Empreendedor)`);
        
        switch (newPersona) {
            case '1':
                currentPersona = 'formal';
                break;
            case '2':
                currentPersona = 'engracada';
                break;
            case '3':
                currentPersona = 'rude';
                break;
            case '4':
                currentPersona = 'empreendedor';
                break;
            default:
                alert("Opção inválida. Mantendo a personalidade atual.");
                break;
        }

        personaNameDisplay.textContent = currentPersona.charAt(0).toUpperCase() + currentPersona.slice(1);
        appendMessage(`Minha personalidade agora é ${currentPersona}.`, 'bot');
    }

    // 6. Eventos
    
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    changePersonaBtn.addEventListener('click', changePersona);
    backToChatBtn.addEventListener('click', hideReport);

    // 7. Início da conversa
    setTimeout(() => {
        appendMessage(respostas.genericas.saudacao[0], 'bot');
        canSendMessage = true;
    }, 1000);
});