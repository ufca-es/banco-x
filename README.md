### Descrição do Bot
Este é um projeto de um chatbot financeiro para o Banco X, desenvolvido como parte da disciplina de Engenharia de Software na UFCA. O chatbot foi construído para responder a perguntas comuns sobre serviços bancários, como Pix, Cartão, Conta e Empréstimo, com diferentes personalidades: formal, engraçada, rude e empreendedor.

O sistema é composto por um backend em Python usando o framework Flask para servir uma aplicação web interativa em HTML, CSS e JavaScript. Ele também gera um relatório de interações para análise.

## Funcionalidades
- Atendimento 24/7
- Personalidades variadas
- Informações sobre serviços bancários básicos
- Salvar histórico de conversas
- Respostas variadas a depender do problema especificado

# Como Executar

1: Dar play no terminal; <br>
2: Selecionar Esclha do Bot (com as emoções); <br>
3: Digitar opções de dúvidas a patir das disponíveis no bot (Transferência, Perda e Tarifas); <br>
4: Para acessar o histórico digitar; <br>
5: Digite sair para finalizar.

Como Instalar e Rodar o Projeto
Siga os passos abaixo para clonar o repositório, configurar o ambiente e executar a aplicação.

1. Clonar o Repositório
Abra o seu terminal e execute o seguinte comando:
```
git clone [https://github.com/ufca-es/banco-x.git](https://github.com/ufca-es/banco-x.git)
cd banco-x
```
2. Configurar o Ambiente Python
Recomendamos usar um ambiente virtual para executar o projeto!

## Cria o ambiente virtual
```
python -m venv venv
```
## Ativa o ambiente virtual
# No Windows:
venv\Scripts\activate
## No macOS e Linux:
source venv/bin/activate

3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias.

pip install Flask pandas matplotlib

4. Executar a Aplicação Web
Certifique-se de que você está na pasta raiz do projeto (banco-x) e execute o arquivo app.py:
```
python app.py
```
O servidor será iniciado em modo de depuração (debug), e você poderá acessar a aplicação no seu navegador através da seguinte URL:
```
http://localhost:5000
```
# Estrutura do Projeto
A estrutura de pastas e arquivos do projeto está organizada da seguinte forma:

```
banco-x/
├── app.py                   # Servidor web principal da aplicação (ponto de entrada).
├── core/
│   ├── chatbot.py           # Lógica principal do chatbot.
│   ├── historico.py         # Gerenciamento do histórico de conversas.
│   ├── main.py              # Lógica de linha de comando (CLI).
│   ├── personalidade.py     # Lida com as personalidades do chatbot.
│   ├── relatorio.py         # Geração dos relatórios de uso.
│   ├── servicos.py          # Lógica para carregar as respostas do chatbot.
│   ├── sugestoes.py         # Gerenciamento de sugestões de perguntas não respondidas.
│   └── utils.py             # Funções utilitárias.
├── data/
│   └── respostasAleatorias.txt # Arquivo de dados com perguntas e respostas.
├── templates/
│   └── index.html           # Arquivo HTML principal da interface web.
└── README.md                # Documentação principal do projeto.
```

# Tecnologias Utilizadas
```
Python 3.x: Linguagem de programação principal.
Flask: Microframework web para Python.
HTML5: Estrutura da página web.
CSS3: Estilização da interface.
JavaScript: Lógica de interação do frontend.
Pandas: Para manipulação de dados na geração do relatório.
Matplotlib: Para visualização de dados no relatório.
```
# Equipe
| Membros  | Funções |
| ------------- | ------------- |
| Ana Aisha  | Desenvolvedor  |
| Elilúcio Teixeira | Desenvolvedor  |
| Samuel Jackson | Desenvolvedor  |
| Sarah Mendes  | Desenvolvedor  |
| ------------- | ------------- |
| Orientador  |
Jayr Alencar Pereira - Professor de Fundamentos da Programação

### data da última atualização do projeto
```
19/09/2025
```
