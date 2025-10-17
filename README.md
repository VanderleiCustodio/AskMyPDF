PDF Chatbot com OpenAI + Qdrant + Streamlit

 Funcionalidades

✔️ Upload de arquivos PDF
✔️ Extração e limpeza de texto com PyPDF
✔️ Divisão inteligente do texto em chunks
✔️ Criação de embeddings com o modelo text-embedding-3-small
✔️ Armazenamento vetorial em Qdrant
✔️ Busca semântica e resposta contextual com GPT-4o
✔️ Interface interativa com Streamlit
✔️ Estilo dark moderno e fluído

Estrutura do Projeto
PDF-Chatbot
├── 📁 Uploaded_pdf/             # Pasta onde os PDFs enviados serão armazenados
├── 📄 app.py                    # Código principal (o que você forneceu)
├── 📄 .env                      # Arquivo com variáveis de ambiente
├── 📄 requirements.txt          # Dependências do projeto
└── 📄 README.md                 # Este arquivo

Instalação e Configuração
Clonar o repositório
git clone https://github.com/seuusuario/pdf-chatbot.git
cd pdf-chatbot

Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

Instalar dependências
pip install -r requirements.txt

4️Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

api_key=YOUR_OPENAI_API_KEY


Dica: Você pode obter sua chave em https://platform.openai.com/api-keys

Configuração do Banco Vetorial (Qdrant)
Instalar e rodar Qdrant (local)

Se ainda não tiver Qdrant instalado, use Docker:

docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant


O app espera o Qdrant rodando em:

http://localhost:6333

Ambiente de Teste Local

Crie uma pasta chamada Uploaded_pdf no mesmo diretório do app (se ainda não existir):

mkdir Uploaded_pdf


Essa pasta será usada automaticamente pelo código para salvar os arquivos enviados pelo Streamlit.

Executando a Aplicação

Inicie o servidor Streamlit:

streamlit run app.py


Acesse no navegador:

http://localhost:8501

Como Usar

Acesse o app no navegador

Faça upload de um arquivo PDF

Aguarde o processamento e vetorização

Faça perguntas sobre o conteúdo do PDF no campo de chat

O assistente responderá com base apenas no conteúdo do documento 

 Principais Classes e Funções
ProcessFile

Responsável por:

Ler e extrair texto dos PDFs

Quebrar em chunks

Gerar embeddings

Criar o contexto de resposta via GPT

Qdrant

Responsável por:

Criar coleção vetorial

Inserir e buscar vetores

Deletar pontos após resposta

Controlar a persistência de embeddings

Requisitos Técnicos
Componente	Versão mínima	Descrição
Python	3.10+	Linguagem principal
Streamlit	1.35+	Interface web
OpenAI	Última versão	API de IA
PyPDF	4.x	Leitura de PDFs
Qdrant	1.10+	Vetor DB
dotenv	1.0+	Variáveis de ambiente
Exemplo de requirements.txt
streamlit
pypdf
langchain-text-splitters
openai
python-dotenv
qdrant-client

Observações Importantes

O Qdrant precisa estar rodando antes de iniciar o Streamlit

Cada sessão limpa os embeddings antigos automaticamente

Ideal para uso em ambiente local de testes
