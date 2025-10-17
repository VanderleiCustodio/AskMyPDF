⚙️ Funcionalidades

✔️ Upload de arquivos PDF
✔️ Extração e limpeza de texto com PyPDF
✔️ Divisão inteligente em chunks de texto
✔️ Criação de embeddings com o modelo text-embedding-3-small
✔️ Armazenamento vetorial em Qdrant
✔️ Busca semântica e respostas contextuais com GPT-4o
✔️ Interface interativa em Streamlit
✔️ Estilo dark moderno e fluido

📁 Estrutura do Projeto
PDF-Chatbot/
├── 📁 Uploaded_pdf/             # Pasta onde os PDFs enviados serão armazenados
├── 📄 app.py                    # Código principal do projeto
├── 📄 .env                      # Arquivo com variáveis de ambiente
├── 📄 requirements.txt          # Dependências do projeto
└── 📄 README.md                 # Este arquivo

🚀 Instalação e Configuração
1️⃣ Clonar o repositório
git clone https://github.com/seuusuario/pdf-chatbot.git
cd pdf-chatbot

2️⃣ Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Configurar variáveis de ambiente

Crie um arquivo chamado .env na raiz do projeto e adicione:

api_key=YOUR_OPENAI_API_KEY


💡 Você pode obter sua chave em:
👉 https://platform.openai.com/api-keys

🗃️ Configuração do Banco Vetorial (Qdrant)

Se ainda não possuir o Qdrant instalado, use Docker:

docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant


O app espera o Qdrant rodando em:

http://localhost:6333

🧪 Ambiente de Teste Local

Crie a pasta onde os PDFs serão armazenados (caso ainda não exista):

mkdir Uploaded_pdf


Essa pasta será utilizada automaticamente pelo código para armazenar os arquivos enviados via Streamlit.

▶️ Executando a Aplicação

Inicie o servidor Streamlit:

streamlit run app.py


Acesse o app no navegador:
👉 http://localhost:8501

💬 Como Usar

Acesse o app no navegador

Faça upload de um arquivo PDF

Aguarde o processamento e vetorização

Digite perguntas no campo de chat

O assistente responderá com base apenas no conteúdo do documento 📘

🧱 Principais Classes e Funções
ProcessFile

Responsável por:

Ler e extrair texto dos PDFs

Dividir o texto em chunks

Gerar embeddings

Criar o contexto de resposta via GPT

Qdrant

Responsável por:

Criar e gerenciar a coleção vetorial

Inserir e buscar vetores

Excluir pontos antigos

Controlar a persistência dos embeddings

🧰 Requisitos Técnicos
Componente	Versão mínima	Descrição
Python	3.10+	Linguagem principal
Streamlit	1.35+	Interface web
OpenAI	Última	API de IA
PyPDF	4.x	Leitura de PDFs
Qdrant	1.10+	Banco vetorial
python-dotenv	1.0+	Variáveis de ambiente
📄 Exemplo de requirements.txt
streamlit
pypdf
langchain-text-splitters
openai
python-dotenv
qdrant-client

⚡ Observações Importantes

O Qdrant deve estar rodando antes de iniciar o Streamlit

Cada sessão limpa os embeddings antigos automaticamente

Ideal para testes locais e experimentação

🌍 Variáveis de Ambiente

O projeto precisa das seguintes variáveis no arquivo .env:

api_key=YOUR_OPENAI_API_KEY


(Outras variáveis podem ser adicionadas futuramente conforme expansão do projeto)
