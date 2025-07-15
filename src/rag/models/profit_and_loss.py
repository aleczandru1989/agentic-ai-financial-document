from enum import Enum
from typing import List
from pydantic import BaseModel, Field
    
class FinancialViewType(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    CONSOLIDATED = "CONSOLIDATED"
    UNKNOWN = "UNKNOWN"

class ValueFormattingType(Enum):
    Thousends= "Thousends",
    Milions= "Milions",
    Bilions= "Billions",
    Trillions= "Trillions",
    UNKNOWN = "UNKNOWN"
    
class Tables(BaseModel):
    financial_view: FinancialViewType = Field(
        description="The type of financial view, can be INDIVIDUAL, CONSOLIDATED, or UNKNOWN"
    )
    currency: str = Field("The type of value, e.g., 'USD', 'EUR'")
    formatting: ValueFormattingType = Field(description="The type of value formatting, can be Thousends, Milions, Bilions, Trillions, or UNKNOWN")
    csv: str = Field("Individual or Consolidated Profit and loss table CSV format")

class ProfitAndLossTables(BaseModel):
    tables: List[Tables] = Field("Individual or Consolidated Profit and Loss tables")
    