import os
from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client import QdrantClient, models
import uuid
import streamlit as st
import random
import time

load_dotenv(find_dotenv())
client_QdrantClient = QdrantClient(url="http://localhost:6333")
client = OpenAI(api_key=f"{os.getenv("api_key")}")

class ProcessFile:
    
    def __init__(self, client):
        self.client = client

    def ReadAndProcess(Self, filename):
        
        Chunks = []
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            
        encoding_name="cl100k_base", chunk_size=1024, chunk_overlap=102) ###

        reader = PdfReader(f"./Uploaded_pdf/{filename}")
        
        for i in reader.pages:
            extracted_text = i.extract_text()
            text = text_splitter.split_text(extracted_text)
            
            for item in text:
                value = item.encode('latin-1', 'ignore').decode('utf-8', 'ignore') ## This gonna Solve  \u00e2\u0080\u0099 problems

                Chunks.append({"Content":f"{value}".replace('\n','')})
        
            
        return Chunks
    
    def Vectorization(self, Chunks):
        
        Vectorized_Document = []
        
        for i in Chunks:
            response = self.client.embeddings.create(
            input=f"{i['Content']}",
            model="text-embedding-3-small" )

            Vectorized_Document.append({"Content":f"{i['Content']}", "Vector": response.data[0].embedding})
            
        return Vectorized_Document
     
    def UserQueryVectorization(self, question):
        
        response = self.client.embeddings.create(
        input=f"{question}",
        model="text-embedding-3-small" )
            
        return response.data[0].embedding
    
    def OpenAiQuestionAnswer(self, user_question, context):
        
            response = self.client.responses.create(
            model="gpt-4o",
            input=f"""
            Você é um assistente inteligente que auxilia
            os funcionários da Contoso, Inc. com dúvidas
            sobre o documento anexado ao chat.
            
            Responda à seguinte pergunta usando <apenas os dados fornecidos no contexto fornecido nas fontes abaixo >.
          
            Pergunta : 
            {user_question}
            
            Fontes de contexto: 
            {context}
            
            """
            )

            return response.output[0].content[0].text
            
class Qdrant:
    def __init__(self, client_QdrantClient):
        
        self.client_QdrantClient = client_QdrantClient
        
    def Create_a_collection(self):
       try: 
                self.client_QdrantClient.create_collection(
                collection_name="HomeChatbot",
                vectors_config=VectorParams(size=1536, distance=models.Distance.COSINE),
            )
       except:
           print(f"___Collection Creation Failed__")
        
        
    def Insert_Vector(self, Vectorized_Document):
        
        for i in Vectorized_Document:
            self.client_QdrantClient.upsert(
            collection_name="HomeChatbot",
            points=[
                models.PointStruct(
                            id= str(uuid.uuid4()), 
                            payload={
                                "Content": f"{i["Content"]}",
                                },
                            vector = i["Vector"]
                            )
            ],
        )
    
    def SearchPoint(self, query):
        rag = ""
        search_result = self.client_QdrantClient.query_points(
        collection_name="HomeChatbot",
        query=query,
        limit=1
        ).points
        
        for i in search_result:
           rag = "".join(i.payload['Content'])
        return rag
    
    def ScrollPoint(self):
        response = self.client_QdrantClient.scroll(
        collection_name="HomeChatbot",
         limit=5000,
        with_payload=False,
        with_vectors=False,
    )
        return response
    
    def deletPoint(self, points_id):
        response = self.client_QdrantClient.delete(
            collection_name="HomeChatbot",
            points_selector=models.PointIdsList(
                points=points_id,
            ),
        )
                  
 
        return response
 
Run_main_Qdrant = Qdrant(client_QdrantClient)
Collection = Run_main_Qdrant.Create_a_collection()

Run_Main_ProcessFile = ProcessFile(client)

upload_folder = "Uploaded_pdf"

uploadfile = st.file_uploader("Select a PDF")

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

if uploadfile is not None:
    filename = uploadfile.name
    savepath = os.path.join(upload_folder,filename)
    
    with open(savepath, 'wb') as f:
        f.write(uploadfile.getbuffer())
        
        Run_def_ReadAndProcess = Run_Main_ProcessFile.ReadAndProcess(filename)
        Vectorization = Run_Main_ProcessFile.Vectorization(Run_def_ReadAndProcess)
        Insert_Vector = Run_main_Qdrant.Insert_Vector(Vectorization)

      
st.markdown("""
    <style>
        /* Fundo geral */
        .stApp {
            background-color: #0d1117;
            color: #e6edf3;
        }

        /* Mensagens do usuário */
        .stChatMessage.user {
            background-color: #1f6feb;
            color: white;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
        }

        /* Mensagens do assistente */
        .stChatMessage.assistant {
            background-color: #161b22;
            color: #d1d5da;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
        }

        /* Input box */
        div[data-testid="stChatInput"] > div > div {
            background-color: #21262d;
            border: 1px solid #30363d;
            color: #f0f6fc;
            border-radius: 8px;
        }

        /* Cursor piscando */
        .cursor {
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            from, to { color: transparent; }
            50% { color: #58a6ff; }
        }
    </style>
""", unsafe_allow_html=True)

# ======== LÓGICA DO APP ========
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Digite sua pergunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)
        
 
    UserQuestionVector = Run_Main_ProcessFile.UserQueryVectorization(prompt)
    searchpoint = Run_main_Qdrant.SearchPoint(UserQuestionVector)
    OpenAiQuestionAnswer = Run_Main_ProcessFile.OpenAiQuestionAnswer(prompt, searchpoint)

    PointsSearch = Run_main_Qdrant.ScrollPoint()
    
    points_id = [
        item.id
        for sublist in PointsSearch
        if isinstance(sublist, list)
        for item in sublist
        if hasattr(item, "id")
    ]
    
    Run_main_Qdrant.deletPoint(points_id)

    with st.chat_message("assistant"):
        with st.spinner("Waiting..."):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = OpenAiQuestionAnswer.strip()

            for char in assistant_response:
                full_response += char
                message_placeholder.markdown(full_response + "<span class='cursor'>▌</span>", unsafe_allow_html=True)
                time.sleep(random.uniform(0.015, 0.035))
            message_placeholder.markdown(full_response, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": full_response})