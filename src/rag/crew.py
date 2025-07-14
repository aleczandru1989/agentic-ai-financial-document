from crewai.tools import tool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from rag.tools.financial_report_period_tool import FinancialReportPeriodTool

@CrewBase
class Rag():
    """Rag crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def financial_report_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_report_classifier'], 
            tools=[FinancialReportPeriodTool()], 
            verbose=True,
            max_attempts=1
        )

    @task
    def financial_report_clasifier_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_report_clasifier_task'],
            max_attempts=1
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Rag crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,   # Enable memory tracking
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
