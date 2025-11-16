from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# 导入项目模块
import models, schemas, crud
from database import engine, get_db

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="题目管理系统")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建题目
@app.post("/api/questions", response_model=schemas.QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    print("question: ", question)
    # 验证数据
    if question.type == "comprehensive":
        if not question.choices or len(question.choices) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="综合知识题必须包含选择题部分"
            )
    elif question.type == "caseAnalysis":
        if not question.subQuestions or len(question.subQuestions) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="案例分析题必须包含小问题部分"
            )
    
    db_question = crud.create_question(db=db, question=question)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建题目失败"
        )
    return db_question

# 获取题目详情
@app.get("/api/questions/{question_id}", response_model=schemas.QuestionResponse)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="题目未找到")
    return db_question

# 获取题目列表
@app.get("/api/questions", response_model=List[schemas.QuestionResponse])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = crud.get_questions(db, skip=skip, limit=limit)
    print(f"获取到 {len(questions)} 道题目")
    
    # 验证并转换为Pydantic模型
    question_responses = [schemas.QuestionResponse.model_validate(question) for question in questions]
    
    question_ids = [question.id for question in question_responses]
    print(f"题目ID列表: {question_ids}")
    
    return question_responses

# 更新题目
@app.put("/api/questions/{question_id}", response_model=schemas.QuestionResponse)
def update_question(question_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    print("question_id: ", question_id)
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="题目未找到")
    
    # 删除原有的题目（包括关联数据）
    db.delete(db_question)
    db.commit()
    
    # 重新创建题目
    updated_question = crud.create_question(db=db, question=question)
    return updated_question

# 删除题目
@app.delete("/api/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="题目未找到")
    
    db.delete(db_question)
    db.commit()
    return {"message": "题目删除成功"}

# 根路径
@app.get("/")
def root():
    return {"message": "题目管理系统API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)