import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from config.llm import llm


class VerificationResult(BaseModel):
    is_correct: bool
    confidence: float
    issues_found: list
    needs_human_review: bool


verifier_prompt = PromptTemplate(
    input_variables=["problem", "solution"],
    template="""
You are a mathematical verification agent.

Check if the provided solution correctly solves the problem.

Evaluate:
- mathematical correctness
- logical reasoning
- edge cases
- final answer correctness

Return ONLY JSON:

{{
 "is_correct": true/false,
 "confidence": 0.0-1.0,
 "issues_found": [],
 "needs_human_review": true/false
}}

Problem:
{problem}

Solution:
{solution}
"""
)


def verify_solution(problem_text, solution):

    chain = verifier_prompt | llm.with_structured_output(VerificationResult)

    result = chain.invoke({
        "problem": problem_text,
        "solution": solution
    })
    
    return result


# TEST
if __name__ == "__main__":

    problem = "Find derivative of x^2 + 3x"
    solution = "The derivative is 2x + 3"

    result = verify_solution(problem, solution)
    
    print(result)