# CrewAI-MultiAgent-Database-Interaction

Flight Database Management System
Sistema intelligente basato su CrewAI per la gestione di un database di prenotazioni voli tramite agenti AI che utilizzano linguaggio naturale.
****Descrizione****
Questo progetto implementa un sistema multi-agente che permette di:

Visualizzare prenotazioni voli esistenti tramite query in linguaggio naturale
Modificare il database (inserire, aggiornare, eliminare prenotazioni)
Integrare un sistema RAG (Retrieval-Augmented Generation) per best practices aeroportuali
Utilizzare guardrail per prevenire allucinazioni e mantenere il contesto

****Architettura****
Componenti Principali
1. Agenti AI (crew.py)

Ricercatore: Esegue query SELECT per visualizzare dati

Modificatore: Gestisce INSERT, UPDATE, DELETE
RAG Agent: Fornisce informazioni da documenti esterni (disabilitato di default)

2. Flow System (main.py)

Router intelligente che determina automaticamente se l'utente vuole visualizzare o modificare
Gestione del flusso conversazionale
Input da riga di comando

3. Tools Personalizzati

list_tables_tool: Elenca tabelle disponibili
tables_schema_tool: Mostra schema e sample data
execute_sql_readonly: Esegue solo query SELECT
execute_sql_write: Esegue INSERT/UPDATE/DELETE
check_sql_tool: Valida la correttezza delle query SQL

4. Guardrail (guardrail.py)

Prevenzione di allucinazioni
Controllo del contesto
Limitazione delle risposte a informazioni verificabili


