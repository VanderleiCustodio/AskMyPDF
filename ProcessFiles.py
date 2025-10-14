import json
import requests
import openai
import os
from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client import QdrantClient, models


load_dotenv(find_dotenv())
client_QdrantClient = QdrantClient(url="http://localhost:6333")
client = OpenAI(api_key=f"{os.getenv("api_key")}")

class ProcessFile:
    
    def __init__(self, client):
        self.client = client

    def ReadAndProcess(Self):
        
        Chunks = []
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            
        encoding_name="cl100k_base", chunk_size=1024, chunk_overlap=102) ###

        reader = PdfReader("./AIArtigue.pdf")
        
        number_of_pages = len(reader.pages)
        
        
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
 
class Qdrant:
    def __init__(self, client_QdrantClient):
        
        self.client_QdrantClient = client_QdrantClient
        
    def Create_a_collection(self):
        
        self.client_QdrantClient.create_collection(
        collection_name="test_collection",
            vectors_config=VectorParams(size=4, distance=models.Distance.COSINE),
        ) 
        
    def Insert_Vector(self, Vectorized_Document):
        
         
        points = [PointStruct(**c) for c in Vectorized_Document]
        
        """
        _____Same As _____
        
        for Campo in Campos:
        operation_info = client.upsert(
        collection_name="LocalChabot",
        wait=True,
        points=[
            PointStruct(**Campo),
    )
        
        """
                
        operation_info = client.upsert(
        collection_name="LocalChabot",
        wait=True,
        points=points,
    )

        return operation_info
    
        
Run_Main_ProcessFile = ProcessFile(client)
Run_def_ReadAndProcess = Run_Main_ProcessFile.ReadAndProcess()
Run_Main_ProcessFile.Vectorization(Run_def_ReadAndProcess)
