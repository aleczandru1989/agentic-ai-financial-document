from pydantic import BaseModel, Field

class ReportPeriod(BaseModel):
    report_year: str = Field(description="The year of the financial report (e.g., '2024')")
    report_type: str = Field(description="The values can be only QUARTER_1, QUARTER_2, QUARTER_3, H1, H2, ANNUAL_REPORT, or OTHER")
    start_date: str = Field(description="The beginning date of the report period")
    to_date: str = Field(description="The end date of the report period")
    reasoning: str = Field(description="Explanation for the classification decision")