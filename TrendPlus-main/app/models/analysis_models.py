from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Input Models
# ---------------------------------------------------------

class UserInput(BaseModel):
    company: str = Field(..., min_length=1)
    role: str = Field(..., min_length=1)
    tech_stack: str = Field(..., min_length=1)
    level: Literal["beginner", "intermediate", "advanced"]
    duration: Literal[7, 15, 30, 45, 60, 90, 120, 150, 180]

# ---------------------------------------------------------
# Internal Models
# ---------------------------------------------------------

class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    published_date: Optional[str] = None

# ---------------------------------------------------------
# AI Output Models (Groq JSON schema)
# ---------------------------------------------------------

class LiveIntelItem(BaseModel):
    title: str
    description: str
    importance: Literal["High", "Medium", "Low"]
    source_urls: List[str]

class InterviewQuestion(BaseModel):
    question: str
    category: Literal["Coding", "Technical", "Aptitude", "HR", "System Design", "Other"]
    difficulty: Literal["Easy", "Medium", "Hard"]
    answer_approach: str
    source_urls: List[str]

class SprintStep(BaseModel):
    number: int
    unit: Literal["Day", "Week"]
    focus: str
    learn: List[str]
    practice: List[str]
    deliverable: str

class Source(BaseModel):
    title: str
    url: str
    published_date: Optional[str] = None

class PlacementReport(BaseModel):
    target_summary: str
    confidence_note: str
    feasibility_assessment: str
    tech_stack_gaps: List[str]
    live_intel: List[LiveIntelItem]
    recent_questions: List[InterviewQuestion]
    sprint_plan: List[SprintStep]
    final_strategy: List[str]
    sources: List[Source]
