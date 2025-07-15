from crewai.tools import tool, BaseTool
from pydantic import BaseModel
from rag.models.report_period import ReportPeriod
from rag.services.rag_service import RagService

class ProfitAnalossExtractorToolInput(BaseModel):
    db_name: str

class ProfitAnalossExtractorTool(BaseTool):
    name: str = "Profit and Loss Extractor Tool"
    description: str = ("Returns info related to profit and loss from report")
    args_schema = ProfitAnalossExtractorToolInput

    def _run(self, db_name: str) -> str:
         rag = RagService(db_name=db_name)
  
         content = rag.search(query="""Retrieve Profit and Loss. Focus on documents containing:
            1. Revenue,
            2. Cost of Goods Sold (COGS),
            3. Gross Profit",
            4. Operating Expenses,
            5."Operating Profit (EBIT),
            6."Interest",
            7."Taxes",
            8."Net Profit""")

         return content
    