🤖 Local Chat Bot

Um chatbot local em Python que processa documentos PDF, gera embeddings com OpenAI e armazena vetores semanticamente em um banco Qdrant.
Ideal para aplicações de IA local, busca semântica e chatbots contextuais baseados em documentos.

🚀 Funcionalidades

📄 Leitura e processamento automático de arquivos PDF

✂️ Divisão inteligente do texto em chunks (usando LangChain Text Splitters)

🧠 Criação de embeddings com o modelo OpenAI text-embedding-3-small

🗄️ Armazenamento dos vetores no Qdrant (banco de dados vetorial local)

⚙️ Totalmente local, ideal para ambientes offline (com API local ou Docker)

🧩 Estrutura do Projeto
Local-Chat-Bot/
├── AIArtigue.pdf           # Documento PDF de exemplo
├── ProcessFiles.py         # Código principal de processamento
├── .env                    # Contém sua API key do OpenAI
├── requirements.txt        # Dependências Python
└── README.md               # Este arquivo

📦 Instalação

Clone o repositório

git clone https://github.com/VanderleiCustodio/Local-Chat-Bot.git
cd Local-Chat-Bot


Crie um ambiente virtual e instale as dependências

python -m venv venv
source venv/bin/activate   # no Windows use: venv\Scripts\activate
pip install -r requirements.txt


Configure o arquivo .env

Crie um arquivo .env na raiz do projeto e adicione sua chave da OpenAI:

api_key=YOUR_OPENAI_API_KEY


Execute o Qdrant localmente

Se você ainda não tem o Qdrant rodando, use Docker:

docker run -p 6333:6333 qdrant/qdrant

🧠 Uso
1️⃣ Processar o PDF e gerar embeddings
python ProcessFiles.py


O script:

Lê o arquivo AIArtigue.pdf

Divide o texto em partes (chunks)

Gera embeddings usando a API da OpenAI

(Opcionalmente) envia esses vetores para o Qdrant

2️⃣ Fluxo principal (resumo)
from ProcessFiles import ProcessFile, Qdrant, client

# Cria processador e gera chunks
processor = ProcessFile(client)
chunks = processor.ReadAndProcess()

# Gera embeddings
vectors = processor.Vectorization(chunks)

# Envia para o Qdrant
db = Qdrant(client)
db.Insert_Vector(vectors)

⚙️ Tecnologias utilizadas
Tecnologia	Descrição
Python 3.10+	Linguagem principal
OpenAI API	Geração de embeddings semânticos
LangChain Text Splitter	Divisão do texto em partes otimizadas
Qdrant	Banco de dados vetorial
PyPDF	Extração de texto de arquivos PDF
dotenv	Gerenciamento de variáveis de ambiente
🧪 Exemplo de saída

Ao rodar o script, os chunks extraídos são processados e cada vetor é armazenado com a seguinte estrutura:

{
  "Content": "Texto processado do PDF...",
  "Vector": [0.35, 0.08, 0.11, 0.44, ...]
}

🛠️ Próximos passos

 Adicionar interface de chat local (com histórico de contexto)

 Implementar busca vetorial no Qdrant

 Suporte a múltiplos PDFs

 Conexão com modelo de geração de resposta (ex: GPT-4-mini local)
