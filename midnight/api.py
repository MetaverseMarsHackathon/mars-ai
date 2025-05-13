from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import make_question  # 설명 생성 함수

app = FastAPI()

class WrongQuestionsRequest(BaseModel):
    incorrectQuestions: List[str]

@app.post("/questions")
async def receive_wrong_questions(request: WrongQuestionsRequest):
    results = []

    for q in request.incorrectQuestions:
        print("❌ 틀린 문제:", q)
        explanation = make_question.make_question(q)  # dict with 'explanation'
        results.append(explanation)

    return {"results": results}
