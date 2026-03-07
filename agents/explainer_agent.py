import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from langchain_core.prompts import PromptTemplate
from config.llm import llm


explainer_prompt = PromptTemplate(
    input_variables=["problem", "solution"],
    template="""
You are a JEE math tutor.

Explain the solution clearly in simple step-by-step form.

Problem:
{problem}

Solution:
{solution}

Explain it like a tutor teaching a student.
"""
)


def explain_solution(problem, solution):

    chain = explainer_prompt | llm

    result = chain.invoke({
        "problem": problem,
        "solution": solution
    })

    return result.content


# TEST
if __name__ == "__main__":

    problem = "Find derivative of x^2 + 3x"

    solution = """
Step 1: derivative of x^2 = 2x
Step 2: derivative of 3x = 3
Final answer: 2x + 3
"""

    explanation = explain_solution(problem, solution)

    print("\nExplanation:\n")
    print(explanation)