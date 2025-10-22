from crewai_tools import TXTSearchTool


tool_rag = TXTSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", 
            config=dict(
                model="llama3.1:latest",
                # temperature=0.5,
            ),
        ),
        embedder=dict(
            provider="ollama", 
            config=dict(
                model="bge-m3:latest",
            ),
        ),
    ), txt = "E:\\crewai_ambienti\\project_work\\project_work_fly\\documento.txt"
)