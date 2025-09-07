from gettext import install
import os
import csv
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Função para validar a entrada de opções
def chat(num_opcoes):
    while True:
        user_input = input().strip()
        if user_input == '0':
            return user_input
        elif user_input in [str(i) for i in range(1, num_opcoes + 1)]:
            return user_input
        else:
            # Permite perguntas fora do script
            return user_input

# Função para registrar interações em um arquivo CSV
def registrar_interacao(persona_nome, pergunta_numero, pergunta_texto):
    with open('log_interacoes.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
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

# Loop principal do chatbot
while True:
    print("\nPor favor selecione a personalidade de atendimento que deseja receber:")
    print("1. Formal e Preciso")
    print("2. Amigável, Acolhedora e Informal")
    print("3. Direto e Rápido")
    print("4. Mentor e Empreendedor")
    print("Digite '0' para sair.")
    
    persona = chat(4)
    if persona == '0':
        print("Sessão encerrada. Obrigado por utilizar nossos serviços.")
        break

    if persona in personas:
        nome_persona, arquivos_resposta = personas[persona]
        print("\n" + mensagens_boas_vindas[persona])
        print("Escolha uma das opções abaixo ou escreva sua dúvida:")
        for k, v in perguntas_fixas.items():
            print(f"{k}. {v}")
        print("Ou escreva sua dúvida diretamente:")

        pergunta = chat(3)

        if pergunta == '0':
            print("Sessão encerrada. Obrigado por utilizar nossos serviços.")
            break

        elif pergunta in perguntas_fixas:
            # Pergunta está no script
            pergunta_texto = perguntas_fixas[pergunta]
            registrar_interacao(nome_persona, pergunta, pergunta_texto)

            file_path = os.path.join(os.path.dirname(__file__), arquivos_resposta[pergunta])
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    conteudo = f.readlines()
                    print(conteudo[2], "\n")
            except FileNotFoundError:
                print("Arquivo de resposta não encontrado. Verifique os arquivos .txt.")
        else:
            # Entrada personalizada (fora do script)
            registrar_interacao(nome_persona, 'N/A', pergunta)
            print("Desculpe, ainda não temos uma resposta para isso. Estamos aprendendo com você!")

    else:
        print("Opção inválida. Tente novamente.")

# Carrega o arquivo de log
try:
    df = pd.read_csv('log_interacoes.csv', encoding='utf-8')
except FileNotFoundError:
    print("Arquivo 'log_interacoes.csv' não encontrado.")
    exit()

# Converte a coluna de data para datetime
df['data_hora'] = pd.to_datetime(df['data_hora'])

# Cria colunas auxiliares para análise
df['dia'] = df['data_hora'].dt.date
df['hora'] = df['data_hora'].dt.hour

# ----------- Relatórios ------------

print("\n===== RELATÓRIO DE USO DO CHATBOT =====\n")

# 1. Total de interações
print(f"🔢 Total de interações registradas: {len(df)}")

# 2. Interações por persona
print("\n👤 Interações por persona:")
print(df['persona'].value_counts())

# 3. Perguntas mais frequentes
print("\n❓ Perguntas mais frequentes:")
print(df['pergunta_texto'].value_counts().head(10))

# 4. Perguntas fora do script
fora_do_script = df[df['pergunta_numero'] == 'N/A']
print(f"\n🚫 Perguntas fora do script: {len(fora_do_script)}")
if not fora_do_script.empty:
    print(fora_do_script[['data_hora', 'persona', 'pergunta_texto']].to_string(index=False))

# 5. Horário de pico (hora com mais atendimentos)
hora_pico = df['hora'].value_counts().idxmax()
print(f"\n⏰ Horário de pico: {hora_pico}:00 horas")

# ----------- Gráficos ------------

# Gráfico de interações por persona
plt.figure(figsize=(6, 4))
df['persona'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Interações por Persona')
plt.xlabel('Persona')
plt.ylabel('Quantidade')
plt.tight_layout()
plt.savefig('grafico_persona.png')
plt.close()

# Gráfico de perguntas mais feitas
plt.figure(figsize=(8, 4))
df['pergunta_texto'].value_counts().head(5).plot(kind='barh', color='orange')
plt.title('Top 5 Perguntas Frequentes')
plt.xlabel('Quantidade')
plt.ylabel('Pergunta')
plt.tight_layout()
plt.savefig('grafico_perguntas.png')
plt.close()

# Gráfico de interações por hora
plt.figure(figsize=(8, 4))
df['hora'].value_counts().sort_index().plot(kind='bar', color='green')
plt.title('Interações por Hora do Dia')
plt.xlabel('Hora')
plt.ylabel('Quantidade')
plt.tight_layout()
plt.savefig('grafico_hora.png')
plt.close()

print("\n📊 Gráficos salvos como:")
print(" - grafico_persona.png")
print(" - grafico_perguntas.png")
print(" - grafico_hora.png")

print("\n✅ Fim do relatório.")
