import sys
import os
import json
import re

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from langchain_core.prompts import PromptTemplate
from config.llm import llm

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


# ----------------------------
# Solver Prompt
# ----------------------------

solver_prompt = PromptTemplate(
    input_variables=["problem", "context"],
    template="""
You are an expert JEE mathematics solver.

Solve the problem EXACTLY as written.

Rules:
- Do NOT change the function
- Do NOT assume missing powers
- Do NOT invent new terms
- Use the exact mathematical expression provided
- Return ONLY the final simplified answer

Problem:
{problem}

Context:
{context}

Return ONLY JSON:

{{
"solution": "final simplified mathematical answer"
}}
"""
)


# ----------------------------
# Extract solution from LLM output
# ----------------------------

def extract_solution(response):

    try:
        data = json.loads(response)
        return data["solution"]

    except:

        match = re.search(r'\{[^{}]*"solution"[^{}]*\}', response)

        if match:
            try:
                data = json.loads(match.group())
                return data["solution"]
            except:
                pass

    return response.split("\n")[-1].strip()


# ----------------------------
# Simplify Expression using SymPy
# ----------------------------

def simplify_expression(expr):

    try:
        expr = expr.replace("^", "**")

        simplified = sp.simplify(parse_expr(expr))

        return str(simplified)

    except:
        return expr


# ----------------------------
# Solver Function
# ----------------------------

def solve_problem(problem, context=""):

    chain = solver_prompt | llm

    result = chain.invoke({
        "problem": problem,
        "context": context
    })

    response = result.content.strip()

    # Extract only solution
    solution = extract_solution(response)

    # Simplify math expression if possible
    solution = simplify_expression(solution)

    return solution


# ----------------------------
# Test
# ----------------------------

# if __name__ == "__main__":

#     problem = "Find derivative of x^2 + 3x"

#     result = solve_problem(problem)

#     print("\nSolution:\n")
#     print(result)