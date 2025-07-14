from crewai.tools import tool, BaseTool
from pydantic import BaseModel
from rag.services.rag_service import RagService

class FinancialReportPeriodToolInput(BaseModel):
    db_name: str

class FinancialReportPeriodTool(BaseTool):
    name: str = "Financial Report Period Tool"
    description: str = ("Returns report year and period content from financial reports")
    args_schema = FinancialReportPeriodToolInput

    def _run(self, db_name: str) -> str:
         rag = RagService(db_name=db_name)
  
         content = rag.search(query="What is the report year and report period?")
        
         return content
    