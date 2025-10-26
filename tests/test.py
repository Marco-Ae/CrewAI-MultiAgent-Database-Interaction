from crewai.flow.flow import Flow, start, listen
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool
)
from langchain_community.utilities.sql_database import SQLDatabase
from crewai import LLM, Agent, Task, Crew, Process
from crewai.tools import tool
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime



load_dotenv("env path")
api_key_gemini = os.getenv('GOOGLE_API_KEY')


llm = LLM(
        provider = "google",
        model = "gemini/gemini-2.5-flash-lite",
        api_key = api_key_gemini,  
        temperature = 0.5,
        )  

db = SQLDatabase.from_uri(database_uri = "dburl path", schema="public")

# Tool CrewAI
@tool("list_tables")
def list_tables_tool() -> str:
    """List the available tables in the DB."""
    return ListSQLDatabaseTool(db=db).invoke("")

@tool("tables_schema")
def tables_schema_tool(tables: str) -> str:
    """Show schema & sample rows for the given tables (comma-separated)."""
    return InfoSQLDatabaseTool(db=db).invoke(tables)

@tool("execute_sql")
def execute_sql_tool(sql_query: str) -> str:
    """Execute a SQL query against the DB. Returns the result as a string."""
    return QuerySQLDatabaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql_tool(sql_query: str) -> str:
    """Check if the SQL query is correct. Returns suggestions/fixes or success message."""
    try:
        query_checker_tool = QuerySQLCheckerTool(db=db, llm=llm)
        return query_checker_tool.invoke(sql_query)
    except Exception as e:
        return f"Error using QuerySQLCheckerTool: {str(e)}"
    

ricercatore = Agent(
    role="Ricercatore di informazioni",
    goal="USANDO I TOOL forniti, raccogliere informazioni sulle persone contenute nella tabella utenti",
    backstory="Esperto di documentazione, specializzato nella ricerca e nell'analisi di dati strutturati",
    llm=llm,
    tools=[list_tables_tool, tables_schema_tool, execute_sql_tool, check_sql_tool],
    verbose=True
)


class SQLmodel(BaseModel):
    file: str = Field(default="", description = "File json con il risultato della ricerca")
    

class Querymodel(SQLmodel):
    risultato: Optional[SQLmodel] = Field( #optional indica che la variabile puo essere di un certo tipo oppure None 
        default = None,
        description = """Risultato strutturato della ricerca."""
    )

    richiesta: Optional[SQLmodel] = Field(
        default = None,
        description = """Ricerca approfondita sulla richiesta"""
    )


class SQLAgentFlow(Flow[Querymodel]):
    @start()
    def ricevi_richiesta(self):
        return "Richiesta ricevuta"

    @listen(ricevi_richiesta)
    def crea_task_ed_esegui(self):
        richiesta = self.state.richiesta

        task_ricercatore = Task(
            description=richiesta,
            expected_output="Risposta dettagliata e coerente con la richiesta.",
            agent=ricercatore,
            output_pydantic = SQLmodel
        )

        crew = Crew(
            agents=[ricercatore],
            tasks=[task_ricercatore],
            process=Process.sequential
        )

        print("Avvio del task con richiesta:", richiesta)
        risultato = crew.kickoff()
        self.state.risultato = risultato
        return "Task completato"

    @listen(crea_task_ed_esegui)
    def riepilogo(self):
        return f"""
                Riepilogo:
                - Richiesta: {self.state.richiesta}
                - Risultato: {self.state.risultato}
            """

if __name__ == "__main__":
    flow = SQLAgentFlow()

    print("Scrivi cosa vuoi sapere dal database (es. 'Mostrami le prenotazioni di Mario'):")
    flow.state.richiesta = input(" ")
    flow.state.risultato = None

    final = flow.kickoff()
    print("\nRisultato finale:")
    print(final)
    print("\nStato finale:")

    print(flow.state)

    filename = "rapporto"

    i = 0
    while os.path.exists(f"C:\\Users\\Abate\\Desktop\\project_work\\project_volo\\logs\\{filename}_{i}.json"):
        i += 1

    with open(f"C:\\Users\\Abate\\Desktop\\project_work\\project_volo\\logs\\{filename}_{i}.json", "w", encoding = "utf-8") as file:
        file.write(flow.state.risultato.model_dump_json(indent = 2))
    print(file.closed)

