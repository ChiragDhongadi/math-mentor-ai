import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from config.llm import llm


class RoutingDecision(BaseModel):
    topic: str
    difficulty: str
    solver_strategy: str


router_prompt = PromptTemplate(
    input_variables=["problem_text"],
    template="""
You are an AI router for a math solving system.

Classify the problem and decide the best solving strategy.

Topics:
- algebra
- calculus
- probability
- linear_algebra

Strategies:
- symbolic_math
- formula_lookup
- algebraic_manipulation
- probability_rules

Return ONLY JSON in this format:

{{
 "topic": "...",
 "difficulty": "easy | medium | hard",
 "solver_strategy": "..."
}}

Problem:
{problem_text}
"""
)


def route_problem(problem_text: str):

    chain = router_prompt | llm.with_structured_output(RoutingDecision)

    result = chain.invoke({"problem_text": problem_text})

    return result


# TEST
if __name__ == "__main__":

    result = route_problem("Find derivative of x^2 + 3x")

    print(result)