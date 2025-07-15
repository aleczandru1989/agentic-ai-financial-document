from crewai.tools import tool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from rag.models.report_period import ReportPeriod
from rag.models.profit_and_loss import ProfitAndLossTables
from rag.tools.financial_report_period_tool import FinancialReportPeriodTool
from rag.tools.profit_and_loss_extractor_tool import ProfitAnalossExtractorTool
import os

@CrewBase
class RagCrew():
    """Rag crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def financial_report_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_report_classifier'], 
            tools=[FinancialReportPeriodTool()], 
            verbose=True,
            max_attempts=1,
            llm=os.getenv("LLM"),
            output_pydantic=ReportPeriod
        )
        
        
    @agent
    def profit_and_loss_extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['profit_and_loss_extractor'], 
            tools=[ProfitAnalossExtractorTool()], 
            verbose=True,
            max_attempts=1,
            llm=os.getenv("LLM"),
            output_pydantic=ProfitAndLossTables
        )

    @task
    def financial_report_clasifier_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_report_clasifier_task'],
            max_attempts=1
        )


    @task
    def profit_and_loss_extractor_task(self) -> Task:
        return Task(
            config=self.tasks_config['profit_and_loss_extractor_task'],
            context=[self.financial_report_clasifier_task()],
            max_attempts=1,
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Rag crew"""
        agents = [
            self.financial_report_classifier(), 
            self.profit_and_loss_extractor()
            ]
        
        return Crew(
            agents=agents,
            tasks=self.tasks, 
            verbose=True,
            process=Process.sequential
        )
