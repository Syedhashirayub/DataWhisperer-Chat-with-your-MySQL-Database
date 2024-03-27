from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import streamlit as st
from sqlalchemy.exc import ProgrammingError
from mysql.connector.errors import ProgrammingError as MySQLProgrammingError

load_dotenv()



def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    try:
        db = SQLDatabase.from_uri(db_uri)
        return db
    except ProgrammingError as e:
        # Handle the case where the database does not exist
        if isinstance(e.orig, MySQLProgrammingError) and e.orig.errno == 1049:
            st.error(f"The database '{database}' does not exist. Please create the database and try again.")
        else:
            st.error("Failed to connect to the database. Please check your connection settings.")
    except Exception as e:
        st.error("An unexpected error occurred.")

def get_sql_chain(db):
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
  prompt = ChatPromptTemplate.from_template(template)
  
  llm = ChatOpenAI(model="gpt-3.5-turbo")
  #llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  
  def get_schema(_):
    return db.get_table_info()
  
  return (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
  )

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
  sql_chain = get_sql_chain(db)

  # Invoke the chain to get the SQL query
  generated_sql_query = sql_chain.invoke({
      "question": user_query,
      "chat_history": chat_history,
  })
  
  # Check if the generated SQL query is valid
  if generated_sql_query.strip().startswith("SELECT") or generated_sql_query.strip().startswith("INSERT") or generated_sql_query.strip().startswith("UPDATE") or generated_sql_query.strip().startswith("DELETE"):
      # Proceed with the execution since the query is valid
      template = """
      You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
      Based on the table schema below, question, sql query, and sql response, write a natural language response and nothing else.
      <SCHEMA>{schema}</SCHEMA>

      Conversation History: {chat_history}
      SQL Query: <SQL>{query}</SQL>
      User question: {question}
      SQL Response: {response}"""
        
      prompt = ChatPromptTemplate.from_template(template)

      llm = ChatOpenAI(model="gpt-3.5-turbo")
        
      chain = (
          RunnablePassthrough.assign(query=lambda _: generated_sql_query).assign(
              schema=lambda _: db.get_table_info(),
              response=lambda vars: db.run(vars["query"]),
          )
          | prompt
          | llm
          | StrOutputParser()
      )

      return chain.invoke({
          "question": user_query,
          "chat_history": chat_history,
      })
  else:
      # The generated SQL query is not valid; return a meaningful message
      return "I'm sorry, I couldn't generate a valid answer based on your question. Could you please rephrase it or ask another question?"
  '''
  template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""
  
  prompt = ChatPromptTemplate.from_template(template)
  
  llm = ChatOpenAI(model="gpt-3.5-turbo")
  #llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
  
  chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
      schema=lambda _: db.get_table_info(),
      response=lambda vars: db.run(vars["query"]),
    )
    | prompt
    | llm
    | StrOutputParser()
  )
  
  return chain.invoke({
    "question": user_query,
    "chat_history": chat_history,
  })
'''
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]



st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon")

st.title("DataWhisperer: Chat with your MySQL Database")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is the simple chat application using MYSQL. Connect to the database and start chatting.")

    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type = "password", key="Password")
    st.text_input("Database", key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to the database..."):
            db = init_database(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            if db is not None:
              st.session_state.db= db
              st.success("Connected to Database")
            

with st.expander("ℹ️ Help & Documentation"):
    st.markdown("""
        <style>
        .docHeader {
            color: #3498db;
            font-weight: bold;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .docSubheader {
            color: #2ecc71;
            font-weight: bold;
            font-size: 20px;
            margin-top: 20px;
            margin-bottom: 5px;
        }
        .docBody {
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .docList {
            margin-left: 20px;
            font-size: 16px;
        }
        </style>

        <div class="docHeader">How to Use This App 📘</div>
        <div class="docBody">
            This app allows you to interact with your MySQL database using natural language. Discover and explore your data with ease.
        </div>

        <div class="docSubheader">Asking Questions 🤔</div>
        <div class="docBody">
            Simply type your question as if you were asking a colleague. For example, <code>"How many orders were placed in January?"</code>
        </div>

        <div class="docSubheader">Examples 💡</div>
        <ul class="docList">
            <li>"What is the average order value for February?"</li>
            <li>"Show me the top 5 products by units sold."</li>
            <li>"List all transactions above $500."</li>
            <li>"How many new customers were acquired last quarter?"</li>
            <li>"Which product category is the most profitable?"</li>
            <li>"Compare this month's revenue to the same month last year."</li>
        </ul>

        <div class="docSubheader">Tips 📌</div>
        <ul class="docList">
            <li>Be as specific as possible with your questions for more accurate answers.</li>
            <li>Review the names of tables and fields in your database to use the correct terminology in your questions.</li>
            <li>Remember, the quality of the generated response depends on how the question is phrased.</li>
        </ul>

        <div class="docBody">
            Dive in and start querying! If you encounter any issues or have feedback, don't hesitate to reach out. Happy data exploring! 😊
        </div>
    """, unsafe_allow_html=True)



for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Ask me about the Database...")

if user_query is not  None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(content=response)) 
elif "db" not in st.session_state:
    #st.session_state.db = None
    st.warning("Database not connected. Please connect to the database first.")