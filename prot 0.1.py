import os  # eu só consegui fazer funcionar a leitura de arquivo txt com o caminho absoluto (localização exata do arquivo) e essa biblioteca permite fazer esse caminho em qualquer computador
def chat(num_opcoes):    # função que recebe o número de opções e retorna a escolhida
    while True:
        try:          # loop de entrada de usuário que garante entradas válidas
            user_input = str(input())
            if user_input in [str(i) for i in range(0, num_opcoes + 1)]:
                return user_input
            else:
                raise ValueError
        except ValueError:
            print("Entrada inválida, por favor insira uma opção adequada.")



while True:
    print("Por favor selecione a personalidade de atendimento que deseja receber: 1. Formal e Preciso ; 2. Amigável, Acolhedora e Informal ; 3. Direto e Rápido ; 4. Mentor e Empreendedor. Caso a qualquer momento deseje sair da conversa, digite '0'.")
    persona = chat(4)

    #SR.BOT
    if persona == '1':   # escolha da personalidade Sr.Bot
        print("""Olá, sou o Sr.Bot, seu assistente da sua sessão de atendimento atual. Em que posso ajudar?
1. Como faço uma transferência via Pix?
2. Perdi meu cartão de débito, o que devo fazer?
3. Onde estão as tarifas da conta corrente?""")
        pergunta = chat(3)
        if pergunta == '1':     # identificação do arquivo txt conta baseado na escolha do usuário
            file_path = os.path.join(os.path.dirname(__file__), 'srbotpix.txt')   # local do arquivo
            with open(file_path, 'r', encoding='utf-8') as f:   # extrai o conteúdo do arquivo
                conteudo = f.readlines()       #leitura do arquivo txt
                print(conteudo[2], "\n") # pergunta 1
                f.close()
                continue
        if pergunta == '2':     
            file_path = os.path.join(os.path.dirname(__file__), 'srbotcartao.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '3':     
            file_path = os.path.join(os.path.dirname(__file__), 'srbotconta.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue

    #CLARA
    elif persona == '2':
        print("""E aí, tudo bem? Eu sou a Clara, sua assistente virtual super legal! Como posso te ajudar hoje?
1. Como faço uma transferência via Pix?
2. Perdi meu cartão de débito, o que devo fazer?
3. Onde ficam as tarifas da conta corrente?""")
        pergunta = chat(3)
        if pergunta == '1':     
            file_path = os.path.join(os.path.dirname(__file__), 'clarapix.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '2':     
            file_path = os.path.join(os.path.dirname(__file__), 'claracartao.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '3':     
            file_path = os.path.join(os.path.dirname(__file__), 'claraconta.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue

    #BYTE
    elif persona == '3':
        print("""Oi, sou o Byte. Do que você precisa?
1. Como faço uma transferência via Pix?
2. Perdi meu cartão de débito, o que devo fazer?
3. Onde ficam as tarifas da conta corrente?""")
        pergunta = chat(3)
        if pergunta == '1':     
            file_path = os.path.join(os.path.dirname(__file__), 'bytepix.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '2':     
            file_path = os.path.join(os.path.dirname(__file__), 'bytecartao.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '3':     
            file_path = os.path.join(os.path.dirname(__file__), 'byteconta.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue

    #MARCOS
    elif persona == '4':
        print("""Olá, me chamo Marcos. Adoraria lhe ajudar em qualquer dúvidas que você tenha, junto de alguns conselhos para sua vida financeira. Sobre o que gostaria de falar?
1. Como faço uma transferência via Pix?
2. Perdi meu cartão de débito, o que devo fazer?
3. Onde ficam as tarifas da conta corrente?""")
        pergunta = chat(3)
        if pergunta == '1':     
            file_path = os.path.join(os.path.dirname(__file__), 'marcospix.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '2':     
            file_path = os.path.join(os.path.dirname(__file__), 'marcoscartao.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue
        if pergunta == '3':     
            file_path = os.path.join(os.path.dirname(__file__), 'marcosconta.txt')   
            with open(file_path, 'r', encoding='utf-8') as f:   
                conteudo = f.readlines()       
                print(conteudo[2], "\n")
                f.close()
                continue

    if persona == '0' or pergunta == '0':  # condição de saída do programa
        print("Sessão encerrada. Obrigado por utilizar nossos serviços.")
        break

    else:
        print("Ainda não possuímos resposta para essa pergunta.Pedimos perdão pelo transtorno. Por favor, selecione outra opção ou digite '0' para sair.")