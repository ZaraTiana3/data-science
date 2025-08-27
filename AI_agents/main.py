import streamlit as st
import time
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import pprint
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores.pgvector import PGVector 
from langchain_core.prompts import PromptTemplate
from project_tools import calcul_prix_revient_benefice_vente
import uuid
import pandas as pd

def stream_data(data):
    for word in data.split():
        yield word + " "
        time.sleep(0.02)

st.title('ChatGPT')

#Initialize session
if "chat_session_id" not in st.session_state: 
    st.session_state.chat_session_id = str(uuid.uuid4())

print("Session id: ",st.session_state.chat_session_id)

#Initialize messages 
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_button_label(chat_df, chat_id):
    first_message = chat_df[(chat_df["ChatID"] == chat_id) & (chat_df["role"] == "user")].iloc[0]["content"]
    return chat_id, ' '.join(first_message.split()[:10])

CSV_FILE = "chat_history.csv"
try:
    chat_history_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    chat_history_df = pd.DataFrame(columns=["ChatID", "role", "content"])

#SIDEBAR
#Upload a file
uploaded_file = st.sidebar.file_uploader("Import a file")

if st.sidebar.button("Start New Chat"):
    st.session_state.chat_session_id = str(uuid.uuid4())
    st.session_state.messages = []

#Previous chats 
st.sidebar.text('Chats')
for chat_id in chat_history_df["ChatID"].unique()[::-1]:
    key_btn, label_btn = get_button_label(chat_history_df, chat_id)
    if st.sidebar.button(label_btn, key=key_btn):
        st.session_state.chat_session_id = chat_id
        loaded_chat = chat_history_df[chat_history_df["ChatID"] == chat_id]
        df = loaded_chat[["role", "content"]]
        result_dict = df.to_dict(orient='records')
        st.session_state.messages = result_dict

#the main program
async def main():
    global chat_history_df
    print("\n Chat history df: ", chat_history_df)
    client = MultiServerMCPClient({
        "postgres": {
           "transport": "sse",
            "url": "http://localhost:8000/sse"
        },
        "tools":{
           "transport": "streamable_http",
            "url": "http://localhost:8001/mcp/"
        },
        "google-calendar": {
           "url": "http://localhost:3000",
            "transport": "streamable_http",
                    }       
    })
    
    #tools
    try:
        tools = await client.get_tools()
    except:
        print('erreurs tools')

    #llm
    key = "Z************************************"
    embeddings =  GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=key)

    llm =  ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", api_key=key)
    
    #Create the agent
    prompt = """
    Tu es un agent intelligent spécialisé dans l’aide à la vente de produits électroniques.
    Ton objectif est de m’aider à maximiser les bénéfices en me donnant des conseils pour augmenter mes ventes.
    Tu as accès à une base de données PostgreSQL, dont le schéma s'appelle 'public'.
    Tu disposes des outils suivants : {tools}, que tu peux utiliser à tout moment pour répondre aux requêtes.
    Par exemple, lorsqu'on te demande d'exécuter une requête dans la base de données et que tu ne connais pas encore les colonnes
    ou les propriétés nécessaires, n’hésite pas à utiliser ces outils pour les rechercher. Cela te permettra ensuite de répondre correctement.
    Utilise les données disponibles pour me proposer des stratégies pertinentes et adaptées.
    """

    agent = create_react_agent(llm, tools, prompt=prompt )

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
        
    #Function to print the messages 
    if prompt:= st.chat_input("Say something"):
        st.chat_message("user").write_stream(stream_data(prompt))
        st.session_state.messages.append({"role":"user", "content":prompt})
        #Add to csv 
        row = {'ChatID': st.session_state.chat_session_id , 'role':'user', 'content':prompt}
        chat_history_df = pd.concat([chat_history_df, pd.DataFrame([row])], ignore_index=True)

        #Assistant
        response = await agent.ainvoke({"messages": prompt})   
        pprint.pprint(response)
        st.chat_message("assistant").write(response['messages'][-1].content)
        st.session_state.messages.append({"role":"assistant", "content":response['messages'][-1].content})
        #ADD TO CSV
        row = {'ChatID': st.session_state.chat_session_id , 'role':'assistant', 'content':response['messages'][-1].content}
        chat_history_df = pd.concat([chat_history_df, pd.DataFrame([row])], ignore_index=True)

        print('\n Messages actuelles:')
        print(st.session_state.messages)

        #save csv
        chat_history_df[['ChatID', 'role', 'content']].to_csv('chat_history.csv')

asyncio.run(main())
