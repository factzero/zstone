from sqlalchemy.orm import Session
import models, schemas

def create_question(db: Session, question: schemas.QuestionCreate):
    # 创建主问题
    db_question = models.Question(
        type=question.type,
        stem=question.stem,
        source=question.source,
        domain=question.domain,
        analysis=question.analysis
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    # 处理选择题部分
    if question.choices and question.type == "comprehensive":
        for choice_data in question.choices:
            db_choice = models.Choice(
                question_id=db_question.id,
                correct_answer=choice_data.correctAnswer
            )
            db.add(db_choice)
            db.commit()
            db.refresh(db_choice)
            
            # 添加选项
            for option_data in choice_data.options:
                db_option = models.Option(
                    choice_id=db_choice.id,
                    text=option_data.text
                )
                db.add(db_option)
            
            db.commit()
    
    # 处理小问题部分
    if question.subQuestions and question.type == "caseAnalysis":
        for sub_q_data in question.subQuestions:
            db_sub_q = models.SubQuestion(
                question_id=db_question.id,
                question_text=sub_q_data.question,
                answer=sub_q_data.answer,
                analysis=sub_q_data.analysis
            )
            db.add(db_sub_q)
        
        db.commit()
    
    return get_question(db, db_question.id)

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()