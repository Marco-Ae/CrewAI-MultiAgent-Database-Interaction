from crewai.tasks.hallucination_guardrail import HallucinationGuardrail
from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv() 
api_key_gemini = os.getenv('GOOGLE_API_KEY')

# ollama = LLM(
#     provider = "ollama",
#     model = "ollama/llama3.1:latest",
#     base_url= "http://localhost:11434", 
#     temperature = 0.3,
#     )  

model = LLM(
    provider = "google",
    model = "gemini/gemini-2.0-flash-lite",
    api_key = api_key_gemini,  
    temperature = 0.3,
    )  

llm = LLM(
    provider = "google",
    model = "gemini/gemini-2.5-flash-lite",
    api_key = api_key_gemini,  
    temperature = 0.0,
    )  


context_guardrail = HallucinationGuardrail(
    context = "#NON FORNIRE INFORMAZIONI CHE NON TROVI, E RIPOSNDI SOLTANTO A ARGOMENTI RIGUARDANTI IL DATABASE",
    llm = LLM(model="gemini-2.0-flash-lite")
)