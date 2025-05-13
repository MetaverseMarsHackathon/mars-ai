from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
os.environ["LANGSMITH_PROJECT"] = "MTVS-11midnight"

# 모델 초기화
model = ChatOpenAI(
    temperature=0.1,
    model="gpt-4.1-nano"
)

# 설명 템플릿
template = """
당신은 초등학생 5학년 과학 선생님입니다.
아래 '상황'은 학생이 잘못 알고 있는 내용입니다. 
왜 틀렸는지 초등학생도 이해할 수 있게 간단하고 정확하게 설명해주세요.

#상황:
{situation}

#FORMAT:
- explanation: [이유 설명]
"""

prompt = PromptTemplate.from_template(template)
output_parser = StrOutputParser()
chain = prompt | model | output_parser

# 설명만 추출
def make_question(wrong_sentence: str) -> dict:
    raw_output = chain.invoke({"situation": wrong_sentence})
    lines = raw_output.strip().splitlines()
    e_line = next((line for line in lines if line.startswith("- explanation:")), "")

    return {
        "explanation": e_line.replace("- explanation:", "").strip()
    }
