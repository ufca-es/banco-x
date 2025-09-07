import os
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import subprocess

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None  # Exibição simples caso não esteja instalado


# Função para validar a entrada de opções
def chat(num_opcoes):
    while True:
        user_input = input().strip().lower()
        if user_input == '0' or user_input == 'relatorio':
            return user_input
        elif user_input in [str(i) for i in range(1, num_opcoes + 1)]:
            return user_input
        else:
            return user_input  # Entrada personalizada


# Função para registrar interações em um arquivo CSV com cabeçalho e separador ';'
def registrar_interacao(persona_nome, pergunta_numero, pergunta_texto):
    file_exists = os.path.isfile('log_interacoes.csv')
    # Usar encoding latin1 para evitar problemas com acentuação em Windows
    with open('log_interacoes.csv', mode='a', newline='', encoding='latin1') as file:
        writer = csv.writer(file, delimiter=';')
        if not file_exists:
            # Escreve o cabeçalho apenas se o arquivo não existir
            writer.writerow(['data_hora', 'persona', 'pergunta_numero', 'pergunta_texto'])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            persona_nome,
            pergunta_numero,
            pergunta_texto
        ])


# Dicionário de perguntas fixas
perguntas_fixas = {
    '1': "Como faço uma transferência via Pix?",
    '2': "Perdi meu cartão de débito, o que devo fazer?",
    '3': "Onde estão as tarifas da conta corrente?"
}

# Mapeia cada persona com seus arquivos de resposta
personas = {
    '1': ("Sr.Bot", {
        '1': 'srbotpix.txt',
        '2': 'srbotcartao.txt',
        '3': 'srbotconta.txt'
    }),
    '2': ("Clara", {
        '1': 'clarapix.txt',
        '2': 'claracartao.txt',
        '3': 'claraconta.txt'
    }),
    '3': ("Byte", {
        '1': 'bytepix.txt',
        '2': 'bytecartao.txt',
        '3': 'byteconta.txt'
    }),
    '4': ("Marcos", {
        '1': 'marcospix.txt',
        '2': 'marcoscartao.txt',
        '3': 'marcosconta.txt'
    })
}

# Mensagens de boas-vindas por persona
mensagens_boas_vindas = {
    '1': "Olá, sou o Sr.Bot, seu assistente da sua sessão de atendimento atual. Em que posso ajudar?",
    '2': "E aí, tudo bem? Eu sou a Clara, sua assistente virtual super legal! Como posso te ajudar hoje?",
    '3': "Oi, sou o Byte. Do que você precisa?",
    '4': "Olá, me chamo Marcos. Adoraria lhe ajudar em qualquer dúvidas que você tenha, junto de alguns conselhos para sua vida financeira. Sobre o que gostaria de falar?"
}


# Função para gerar relatório
def gerar_relatorio():
    print("\n===== RELATÓRIO DE USO DO CHATBOT =====\n")
    try:
        # Ler CSV com separador ; e encoding latin1 para Windows
        df = pd.read_csv('log_interacoes.csv', encoding='latin1', delimiter=';')
    except FileNotFoundError:
        print("Arquivo 'log_interacoes.csv' não encontrado.")
        return
    except pd.errors.ParserError:
        print("Erro ao ler o arquivo CSV. Verifique se o arquivo está no formato correto.")
        return

    # Verifica se o cabeçalho esperado está presente
    colunas_esperadas = ['data_hora', 'persona', 'pergunta_numero', 'pergunta_texto']
    if not all(col in df.columns for col in colunas_esperadas):
        print(f"Erro: Cabeçalho não encontrado no arquivo CSV.")
        print(f"Colunas encontradas: {list(df.columns)}")
        return

    df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
    df.dropna(subset=['data_hora'], inplace=True)  # Remove linhas com data inválida
    df['dia'] = df['data_hora'].dt.date
    df['hora'] = df['data_hora'].dt.hour

    print(f"Total de interações registradas: {len(df)}")

    print("\nInterações por persona:")
    print(df['persona'].value_counts())

    print("\nPerguntas mais frequentes:")
    print(df['pergunta_texto'].value_counts().head(10))

    fora_do_script = df[df['pergunta_numero'] == 'N/A']
    print(f"\nPerguntas fora do script: {len(fora_do_script)}")
    if not fora_do_script.empty:
        if tabulate:
            print(tabulate(fora_do_script[['data_hora', 'persona', 'pergunta_texto']],
                           headers='keys', tablefmt='grid', showindex=False))
        else:
            print(fora_do_script[['data_hora', 'persona', 'pergunta_texto']].to_string(index=False))

    hora_pico = df['hora'].value_counts().idxmax()
    print(f"\nHorário de pico: {hora_pico}:00 horas")

    # ----------- Gráficos ------------
    plt.figure(figsize=(6, 4))
    df['persona'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Interações por Persona')
    plt.xlabel('Persona')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    plt.savefig('grafico_persona.png')
    plt.close()

    plt.figure(figsize=(8, 4))
    df['pergunta_texto'].value_counts().head(5).plot(kind='barh', color='orange')
    plt.title('Top 5 Perguntas Frequentes')
    plt.xlabel('Quantidade')
    plt.ylabel('Pergunta')
    plt.tight_layout()
    plt.savefig('grafico_perguntas.png')
    plt.close()

    plt.figure(figsize=(8, 4))
    df['hora'].value_counts().sort_index().plot(kind='bar', color='green')
    plt.title('Interações por Hora do Dia')
    plt.xlabel('Hora')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    plt.savefig('grafico_hora.png')
    plt.close()

    print("\nGráficos salvos como:")
    print(" - grafico_persona.png")
    print(" - grafico_perguntas.png")
    print(" - grafico_hora.png")

    # Perguntar se quer abrir o Excel
    while True:
        abrir_excel = input("\nDeseja abrir o arquivo de relatório (log_interacoes.csv) no Excel? (s/n): ").strip().lower()
        if abrir_excel == 's':
            try:
                # Comando para abrir arquivo no Excel no Windows
                os.startfile('log_interacoes.csv')
            except Exception as e:
                print(f"Não foi possível abrir o Excel automaticamente: {e}")
            break
        elif abrir_excel == 'n':
            break
        else:
            print("Digite 's' para sim ou 'n' para não.")


# ---------- Validação dos arquivos de resposta ----------
print("Validando arquivos de resposta...")
missing_files = []
for _, arquivos in personas.values():
    for path in arquivos.values():
        if not os.path.exists(path):
            missing_files.append(path)

if missing_files:
    print("Atenção: Os seguintes arquivos estão ausentes:")
    for f in missing_files:
        print(f" - {f}")
    print("Por favor, adicione os arquivos antes de continuar.\n")

# ---------- Loop Principal ----------
while True:
    print("\nDigite 'relatorio' para gerar relatório de uso, ou selecione uma personalidade para atendimento.")
    print("1. Formal e Preciso")
    print("2. Amigável, Acolhedora e Informal")
    print("3. Direto e Rápido")
    print("4. Mentor e Empreendedor")
    print("Digite '0' para sair.")
    op = input().strip().lower()

    if op == 'relatorio':
        gerar_relatorio()
        continue

    if op == '0':
        print("Sessão encerrada. Obrigado por utilizar nossos serviços.")
        gerar_relatorio()
        break

    if op in personas:
        nome_persona, arquivos_resposta = personas[op]
        print("\n" + mensagens_boas_vindas[op])
        print("Escolha uma das opções abaixo ou escreva sua dúvida:")
        for k, v in perguntas_fixas.items():
            print(f"{k}. {v}")
        print("Ou escreva sua dúvida diretamente:")

        pergunta = chat(3)

        if pergunta == '0':
            print("Sessão encerrada. Obrigado por utilizar nossos serviços.")
            gerar_relatorio()
            break

        elif pergunta in perguntas_fixas:
            pergunta_texto = perguntas_fixas[pergunta]
            registrar_interacao(nome_persona, pergunta, pergunta_texto)

            file_path = arquivos_resposta.get(pergunta)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    conteudo = f.read().strip()
                    print("\n" + conteudo + "\n")
            except FileNotFoundError:
                print("Arquivo de resposta não encontrado. Verifique os arquivos .txt.")
        else:
            registrar_interacao(nome_persona, 'N/A', pergunta)
            print("Desculpe, ainda não temos uma resposta para isso. Estamos aprendendo com você!")

    else:
        print("Opção inválida. Tente novamente.")
