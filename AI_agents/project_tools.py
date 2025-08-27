from typing import List
from mcp.server.fastmcp import FastMCP
import pandas as pd
import datetime
from pydantic import BaseModel, Field
from typing import List
import datetime
from psycopg import Connection
from typing import Tuple
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres import PostgresStore
import uuid

mcp = FastMCP(name="tools", host="127.0.0.1", port=8001)

@mcp.tool()
async def calculatrice(operation: str, a: float, b: float) -> str:
    """
    Effectue une opération mathématique de base entre deux nombres, les operations possible sont addition, soustraction, multiplication ou division.
    """
    if operation == "addition":
        result = a + b
    elif operation == "soustraction":
        result = a - b
    elif operation == "multiplication":
        result = a * b
    elif operation == "division":
        if b == 0:
            return "Erreur : division par zéro."
        result = a / b
    else:
        return "Opération non reconnue."

    return f"Le résultat de {operation} entre {a} et {b} est {result}."

@mcp.tool()
def create_memory(index_value: str, memory: str):
    """
    Outil aidant dans la création de memoire 
    - index_value est un parametre a fournir pour preciser la nature de la memoire a enregistrer , par exemple rappel ou opportunité vente, .....
    - memory c'est la memoire a stocker
    
    """
    #Initialisation de la memorire 
    DB_URI = "postgresql://postgres:example@localhost:15432/postgres?sslmode=disable"
    connection_kwargs = {"autocommit": True, "prepare_threshold": 0,
    }
    conn =  Connection.connect(DB_URI, **connection_kwargs)
    embeddings =  GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyBixXBp6k1wDIG1VHOrw3SMygX8Fn7xg3w")
    #embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-distilroberta-v1")
    store = PostgresStore(conn, index={"embed": embeddings, "dims": 768})
    store.setup()

    user_id = "Mikeza"
    namespace_for_memory = (user_id, "memories")

    store.put( namespace_for_memory,
            str(uuid.uuid4()),
            {index_value: memory},
            index=[index_value]
    )
    return 'Memoire stockée'

@mcp.tool()
def search_memory(query: str):
    """
    Outil aidant dans la recherche de memoire 
    - query  correspond à ce qu'on recherche  dans le store 
    
    """
    #Initialisation de la memorire 
    DB_URI = "postgresql://postgres:example@localhost:15432/postgres?sslmode=disable"
    connection_kwargs = {"autocommit": True, "prepare_threshold": 0,
    }
    conn =  Connection.connect(DB_URI, **connection_kwargs)
    embeddings =  GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyBixXBp6k1wDIG1VHOrw3SMygX8Fn7xg3w")
    #embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-distilroberta-v1")
    store = PostgresStore(conn, index={"embed": embeddings, "dims": 768})
    store.setup()

    user_id = "Mikeza"
    namespace_for_memory = (user_id, "memories")

    memories = store.search(
        namespace_for_memory,
        query=query,
        limit=8)
    
    return memories

@mcp.tool()
async def calcul_prix_revient_benefice_vente(content:str) -> str:
    """
    Calcule les totaux de prix de revient, prix de vente et bénéfice à partir d'une liste de ventes.
     Pour chaque produit :
    - Calcule le prix de revient total, le prix de vente total, et le bénéfice.
    Ajoute une ligne "Total" avec les sommes globales.

    Entrée : un string
    Sortie : un string
    """
    print(content)
    data = eval(content)
    df = pd.DataFrame(data)
    df = df[['date','nom_produit','quantite','prix_revient','prix_vente']]
    df = df.rename(columns={"prix_revient": "prix_revient_unitaire", "prix_vente": "prix_vente_unitaire"})
    df['benefice_unitaire'] = df["prix_vente_unitaire"] - df["prix_revient_unitaire"]
    df['prix_revient'] = df["prix_revient_unitaire"]*df['quantite']
    df['prix_vente'] = df["prix_vente_unitaire"]*df['quantite']
    df["benefice"] = df["prix_vente"] - df["prix_revient"]

    ligne_total = {'date': '','nom_produit': 'Total',
                'quantite': df['quantite'].sum(),
                'prix_revient_unitaire':df['prix_revient_unitaire'].sum(),
                'prix_vente_unitaire': df['prix_vente_unitaire'].sum(),
                'benefice_unitaire': df['benefice_unitaire'].sum(),
                'prix_revient': df['prix_revient'].sum(), 
                'prix_vente':df['prix_vente'].sum(),
                'benefice':df['benefice'].sum(),
                    }
    df = pd.concat([df, pd.DataFrame([ligne_total])], ignore_index=True)
    markdown_table = df.to_markdown(index=False, tablefmt="github")
    print(markdown_table)
    return markdown_table
