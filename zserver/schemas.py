from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class QuestionTypeEnum(str, Enum):
    COMPREHENSIVE = "comprehensive"
    CASE_ANALYSIS = "caseAnalysis"
    THESIS = "thesis"

class OptionCreate(BaseModel):
    text: str

    class Config:
        from_attributes = True

class OptionResponse(OptionCreate):
    id: int
    choice_id: int

class ChoiceCreate(BaseModel):
    options: List[OptionCreate]
    correctAnswer: int

    class Config:
        from_attributes = True

class ChoiceResponse(BaseModel):
    id: int
    question_id: int
    options: List[OptionResponse]
    correctAnswer: int = Field(alias="correct_answer", serialization_alias="correctAnswer")

    class Config:
        from_attributes = True

class SubQuestionCreate(BaseModel):
    question: str
    answer: str
    analysis: Optional[str] = None

    class Config:
        from_attributes = True

class SubQuestionResponse(BaseModel):
    id: int
    question_id: int
    question: str = Field(alias="question_text", serialization_alias="question")
    answer: str
    analysis: Optional[str] = None

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    type: QuestionTypeEnum
    stem: str
    source: Optional[str] = None
    domain: Optional[str] = None
    choices: Optional[List[ChoiceCreate]] = None
    subQuestions: Optional[List[SubQuestionCreate]] = None
    analysis: Optional[str] = None

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    type: str
    stem: str
    source: Optional[str] = None
    domain: Optional[str] = None
    choices: Optional[List[ChoiceResponse]] = None
    subQuestions: Optional[List[SubQuestionResponse]] = Field(alias="sub_questions", serialization_alias="subQuestions")
    analysis: Optional[str] = None

    class Config:
        from_attributes = True