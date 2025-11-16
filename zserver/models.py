from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)
    stem = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)
    domain = Column(String(255), nullable=True)
    analysis = Column(Text, nullable=True)
    
    # 关系
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")
    sub_questions = relationship("SubQuestion", back_populates="question", cascade="all, delete-orphan")

class Choice(Base):
    __tablename__ = "choices"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    correct_answer = Column(Integer, nullable=False)  # 存储索引号而不是字母
    
    # 关系
    question = relationship("Question", back_populates="choices")
    options = relationship("Option", back_populates="choice", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"
    
    id = Column(Integer, primary_key=True, index=True)
    choice_id = Column(Integer, ForeignKey("choices.id"), nullable=False)
    text = Column(Text, nullable=False)
    
    # 关系
    choice = relationship("Choice", back_populates="options")

class SubQuestion(Base):
    __tablename__ = "sub_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    analysis = Column(Text, nullable=True)
    
    # 关系
    question = relationship("Question", back_populates="sub_questions")