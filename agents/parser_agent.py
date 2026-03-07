import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List
from config.llm import llm


class ParsedProblem(BaseModel):
    problem_text: str
    topic: str
    variables: List[str]
    constraints: List[str]
    needs_clarification: bool


parser_prompt = PromptTemplate(
    input_variables=["input_text"],
    template="""
You are a math problem parser.

Clean and structure the following math question.

Extract:
- clean problem text
- topic (algebra, calculus, probability, linear algebra)
- variables
- constraints
- detect if clarification is needed

Return ONLY valid JSON in this format:

{{
 "problem_text": "...",
 "topic": "...",
 "variables": [],
 "constraints": [],
 "needs_clarification": false
}}

Question:
{input_text}
"""
)


def parse_problem(input_text: str):

    chain = parser_prompt | llm.with_structured_output(ParsedProblem)

    result = chain.invoke({"input_text": input_text})

    return result


# TEST
if __name__ == "__main__":

    result = parse_problem("Find derivative of x^2 + 3x")

    print(result)