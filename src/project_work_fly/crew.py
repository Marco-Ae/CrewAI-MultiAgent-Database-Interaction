from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import Agent, Crew, Task, Process
from crewai.tools import tool
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool
)
from langchain_community.utilities.sql_database import SQLDatabase
from crewai.tasks.conditional_task import ConditionalTask
from project_work_fly.rag_tool import tool_rag
from project_work_fly.guardrail import model, context_guardrail, llm


db = SQLDatabase.from_uri(database_uri = "db path url", schema="public")
    

@tool("list_tables")
def list_tables_tool() -> str:
    """List the available tables in the DB.""" #tutti e due
    return ListSQLDatabaseTool(db=db).invoke("")

@tool("tables_schema")
def tables_schema_tool(tables: str) -> str:
    """Show schema & sample rows for the given tables (comma-separated)."""
    return InfoSQLDatabaseTool(db=db).invoke(tables)

# @tool("execute_sql")
# def execute_sql_tool(sql_query: str) -> str:
#     """Execute a SQL query against the DB. Returns the result as a string.""" #ricercatore
#     return QuerySQLDatabaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql_tool(sql_query: str) -> str:
    """Check if the SQL query is correct. Returns suggestions/fixes or success message."""
    try:
        query_checker_tool = QuerySQLCheckerTool(db=db, llm=llm)
        return query_checker_tool.invoke(sql_query)
    except Exception as e:
        return f"Error using QuerySQLCheckerTool: {str(e)}"
    
@tool("execute_sql_readonly")
def execute_sql_readonly(sql_query: str) -> str:
    """
    Execute a READ-ONLY SQL query (SELECT only).
    Returns the result as a string.
    """
    query_upper = sql_query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return "ERRORE: Questo tool può eseguire solo query SELECT."
    
    return QuerySQLDatabaseTool(db=db).invoke(sql_query)

@tool("execute_sql_write")
def execute_sql_write(sql_query: str) -> str:
    """
    Execute a WRITE SQL query (INSERT, UPDATE, DELETE).
    Returns the result as a string.
    USE WITH CAUTION!
    """
    query_upper = sql_query.strip().upper()
    if query_upper.startswith("SELECT"):
        return "ERRORE: Questo tool NON può eseguire SELECT."
    
    allowed = ["INSERT", "UPDATE", "DELETE"]
    if not any(query_upper.startswith(cmd) for cmd in allowed):
        return "ERRORE: Query non permessa. Usa solo INSERT, UPDATE o DELETE."
    
    return QuerySQLDatabaseTool(db=db).invoke(sql_query)



#custom tool sono execute_sql_write e quella del read, perche ho visto che tolto execute_sql, non riesce a visualizzare al roba nel db
#e quindi serviva per forza, allora a sto punto sia modificatore che visualizzatore usavato execute, cosi ho trovato dei custom tool
#che fanno o solo write o solo read del db, in base alla richiesta utente.

#rag: la rag funziona ma attualmente l'agente non viene richiamato nel main, perche era troppo lento anche con rag etc, quindi
#l'ho disattivata ma funziona se riattivata, restituisce il json e le best practice da seguire negli aereoporti europei.


#nel file utilizzo il return task infondo invece di farlo all'inizio perche' visivamente si legge meglio, dove iniza e finisce
    
class SQLmodel(BaseModel): #primo base model, l'altro sta nel main.
    nome_cognome: str = Field(default = "", description = "NOME e #COGNOME dell'utente nel file json con il risultato della ricerca")
    numero_volo: str = Field(default = "", description = "#NUMERO del VOLO ad ESEMPIO: AF...")
    bagaglio_incluso: str = Field(default = "", description = "#BAGAGLIO INCLUSO o NO")
    partenza_destinazione: str = Field(default = "", description = "PARTENZA da e DESTINAZIONE")
    volo_data: str = Field(default = "", description = "#DATA di PARTENZA")
    data_registrazione: str = Field(default = "", description = "#DATA di REGISTRAZIONE")
    prezzo: float = Field(default = "", description = "#PREZZO DEL BIGLIETTO")
    aereoporto_partenza_arrivo: str = Field(default = "", description = "#AEREOPORTO DI PARTENZA e DI ARRIVO")
    email_valida: str = Field(default = "", description = "#VERIFICA SE L'EMAIL valida, rispondi con True o False")


 
@CrewBase
class ProjectVolo(): 

    agents: List[BaseAgent]
    tasks: List[Task]

    task_config = "config/tasks.yaml"
    agent_config = "config/agents.yaml"

        
    @agent
    def ricercatore(self) -> Agent:
        return Agent(
            config=self.agents_config['ricercatore'], 
            verbose=True,
            llm = llm,
            tools=[list_tables_tool, tables_schema_tool, execute_sql_readonly, check_sql_tool],
    
        )

    @agent
    def modificatore(self) -> Agent:
        return Agent(
            config=self.agents_config['modificatore'], 
            verbose=True,
            llm = llm,
            tools=[list_tables_tool, tables_schema_tool, execute_sql_write, check_sql_tool]
        )



    @agent
    def rag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['rag_agent'], 
            verbose=True,
            llm = model,
            tools = [tool_rag],
        )
    

    @task
    def esegui_ricerca(self):
        task = Task(
            config=self.tasks_config['task_ricercatore'],
            output_pydantic = SQLmodel,
            output_file = "save file path",
            guardrail = context_guardrail
        )

        return task 

    @task
    def task_modifica(self) -> Task:
        task = Task(
            config=self.tasks_config['task_modifica'], 
            output_pydantic = SQLmodel,
            output_file = "save file path",
            guardrail = context_guardrail
        )

        return task
    
    @task
    def task_rag(self):
        task = Task(
            config=self.tasks_config['task_rag'], 
            output_file = "save file path",
            tools = [tool_rag],
            guardrail = context_guardrail
        )


        return task
    
    @task
    def task_saluto(self):
        """Saluta l'utente solo se è stato trovato nel database"""
        task = ConditionalTask(
            config=self.tasks_config['task_saluto'],
            condition = lambda context: "non trovato" not in str(context).lower()
        )

        return task

    @crew
    def crew(self) -> Crew:

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
