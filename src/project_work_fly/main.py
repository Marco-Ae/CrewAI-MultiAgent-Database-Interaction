import warnings
from crewai.flow.flow import Flow, listen, router, start
from project_work_fly.crew import ProjectVolo
from pydantic import BaseModel, Field
from crewai import Process, Crew
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


class FlowState(BaseModel):
    richiesta: str = Field(default="", description="Richiesta dell'utente")


class DatabaseFlow(Flow[FlowState]):

    @start()
    def ricevi_richiesta(self):


        print("Scrivi cosa vuoi fare ad esempio Mostrami le prenotazioni di luca o aggiungi una prenotazione:")

        self.state.richiesta = input("> ")
        
        if not self.state.richiesta:
            print("Errore: richiesta vuota")
            return None
            
        print(f"\nRichiesta ricevuta: {self.state.richiesta}")
        return "richiesta_processata"

    @router(ricevi_richiesta)
    def determina_azione(self):
        richiesta_lower = self.state.richiesta.lower()

        parole_modifica = [
            "aggiungere", "aggiungi", "inserire", "inserisci", 
            "modificare", "modifica", "cambiare", "cambia",
            "sostituire", "sostituisci", "aggiornare", "aggiorna",
            "cancellare", "cancella", "eliminare", "elimina"
        ]
        
        if any(parola in richiesta_lower for parola in parole_modifica):
            print("MODIFICA DATABASE")
            return "modificare"
        else:
            print("VISUALIZZA DATABASE")
            return "visualizzare"

    @listen("visualizzare")
    def esegui_visualizzazione(self):
        print("\nMODALITÀ VISUALIZZAZIONE")
        print("Esecuzione ricerca nel database...")
        
        try:
            inputs = {'topic': self.state.richiesta}
            
            project = ProjectVolo()
            #crew_instance = project.crew()

            crew_instance = Crew(
                agents=[project.ricercatore()],
                tasks=[project.esegui_ricerca(), project.task_saluto()],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew_instance.kickoff(inputs=inputs)
            #self.state.risultato = str(result)
            
            
        except Exception as e:
            print(f"\nErrore durante la visualizzazione: {e}")
            #self.state.risultato = f"Errore: {str(e)}"
        
        return "completato"

    @listen("modificare")
    def esegui_modifica(self):
        print("\nMODALITÀ MODIFICA")
        print("Esecuzione modifica del database...")
        
        try:
            inputs = {'topic': self.state.richiesta}
            
            project = ProjectVolo()
            #crew_instance = project.crew()

            crew_instance = Crew(
                agents=[project.modificatore()],
                tasks=[project.task_modifica()],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew_instance.kickoff(inputs=inputs)
            #self.state.risultato = str(result)
            
        except Exception as e:
            print(f"\nErrore durante la modifica: {e}")
        
        return "completato"


def run():
    try:
        flow = DatabaseFlow()
        flow.kickoff()
    except KeyboardInterrupt:
        print("\n\nOperazione annullata dall'utente.")
    except Exception as e:
        print(f"\nErrore critico: {e}")
        raise



if __name__ == "__main__":
        run()

