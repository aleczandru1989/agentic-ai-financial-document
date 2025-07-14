#!/usr/bin/env pyt
import warnings
from rag.crew import Rag
from rag.services.rag_builder_service import RagBuilderService
import os
from phoenix.otel import register
from openinference.instrumentation.crewai import CrewAIInstrumentor


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    
    try:
        
        init_tracing()
        
        content = create_rag__db('SAFE_2024')
        
        inputs = {
            'content': content,
            'db_name': 'SAFE_2024'
        }
        

        Rag().crew().kickoff(inputs=inputs)
            
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    
def create_rag__db(db_name: str):
    with open(f"resources/vectorstores/{db_name}.md", "r", encoding="utf-8") as file:
        content = file.read()
        
        rag_service = RagBuilderService(markdown=content, db_name=db_name)
        
        rag_service.create_rag_db()
        
        return content


def init_tracing():
    phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006")
    
    print(phoenix_endpoint)
    
    tracer_provider = register(
        project_name="crewai-rag",
        endpoint=f"{phoenix_endpoint}/v1/traces",  # Phoenix register handles the path automatically
        auto_instrument=True,
    )
    
    CrewAIInstrumentor().instrument(skip_dep_check=True, tracer_provider=tracer_provider)
    
    return tracer_provider