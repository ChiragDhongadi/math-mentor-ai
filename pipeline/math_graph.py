import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import TypedDict, Optional
from agents.parser_agent import parse_problem
from agents.router_agent import route_problem
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution
from langgraph.graph import StateGraph, START, END
from memory.memory_store import retrieve_similar, store_memory
from multimodal.ocr import extract_text_from_image
from multimodal.audio import transcribe_audio
from rag.retriever import retrieve_context


class MathState(TypedDict, total=False):

    input_type: str

    text_input: Optional[str]

    image_path: Optional[str]

    audio_path: Optional[str]

    input_text: Optional[str]

    parsed_problem: dict
    routing: dict
    solution: str
    verification: dict
    explanation: str
    memory_used: bool
    retrieved_context: list
    hitl_required: bool
    hitl_reason: str
    force_hitl: bool 


def input_router(state: MathState):

    return state["input_type"]


def text_node(state: MathState):

    return {
        "input_text": state["text_input"]
    }

def image_node(state: MathState):

    text, confidence = extract_text_from_image(state["image_path"])

    print("OCR Extracted:", text)

    hitl_required = False
    hitl_reason = ""

    if confidence < 0.6:

        hitl_required = True
        hitl_reason = "Low OCR confidence"

    return {
        "input_text": text,
        "hitl_required": hitl_required,
        "hitl_reason": hitl_reason
    }

def audio_node(state: MathState):

    text, confidence = transcribe_audio(state["audio_path"])

    hitl_required = False
    hitl_reason = ""

    if confidence < 0.6:

        hitl_required = True
        hitl_reason = "Low ASR confidence"

    return {
        "input_text": text,
        "hitl_required": hitl_required,
        "hitl_reason": hitl_reason
    }


def parser_node(state: MathState):

    parsed = parse_problem(state["input_text"])
    
    hitl_required = state.get("hitl_required", False)
    hitl_reason = state.get("hitl_reason", "")

    # Trigger HITL if parser detects ambiguity (e.g. empty or very short text)
    if not parsed.problem_text or len(parsed.problem_text.strip()) < 3:
        hitl_required = True
        if hitl_reason:
            hitl_reason += "; "
        hitl_reason += "Parser detected ambiguity"

    return {"parsed_problem": parsed.model_dump(), "hitl_required": hitl_required, "hitl_reason": hitl_reason}


def router_node(state: MathState):

    problem = state["parsed_problem"]["problem_text"]

    routing = route_problem(problem)

    return {"routing": routing.model_dump()}


def solver_node(state: MathState):

    problem = state["parsed_problem"]["problem_text"]

    # --------------------------
    # Retrieve similar problems from memory
    # --------------------------
    similar = retrieve_similar(problem)

    # Short-circuit: If we have an exact verified match, use it directly.
    if similar:
        top_score, top_q, top_sol, top_ver = similar[0]
        # Score > 0.99 implies identical question. Check if it was human verified.
        if top_score > 0.99 and (top_ver.get("corrected_by_human") or top_ver.get("human_verified")):
            print(f"Exact verified match found (score: {top_score:.4f}). Using stored solution.")
            return {
                "solution": top_sol,
                "memory_used": True,
                "retrieved_context": []
            }

    memory_context = ""

    if similar:

        print("Similar problems found in memory")

        for score, q, sol, verification in similar:
            
            label = "Similar solved problem"
            if verification.get("corrected_by_human") or verification.get("human_verified"):
                label = "VERIFIED HUMAN SOLUTION (High Confidence)"

            memory_context += f"""
Example ({label}):

Problem: {q}
Final Answer: {sol}
"""

    # --------------------------
    # Retrieve RAG knowledge
    # --------------------------
    docs = retrieve_context(problem)

    rag_context = "\n".join([doc.page_content for doc in docs])

    # --------------------------
    # Combine all context
    # --------------------------
    full_context = f"""
Relevant formulas:
{rag_context}

Past solved examples:
{memory_context}
"""

    # --------------------------
    # Generate new solution
    # --------------------------
    solution = solve_problem(problem, full_context)

    return {
        "solution": solution,
        "memory_used": bool(similar),
        "retrieved_context": [doc.page_content for doc in docs]
    }

def verifier_node(state: MathState):

    problem = state["parsed_problem"]["problem_text"]
    solution = state["solution"]

    verification = verify_solution(problem, solution)

    print("Verifier result:", verification.model_dump())

    hitl_required = state.get("hitl_required", False)
    hitl_reason = state.get("hitl_reason", "")

    # Low confidence from verifier
    if verification.confidence < 0.7:
        hitl_required = True
        if hitl_reason:
            hitl_reason += "; "
        hitl_reason += "Low verifier confidence"

    # Verifier explicitly asks for human review
    if verification.needs_human_review:
        hitl_required = True
        if hitl_reason:
            hitl_reason += "; "
        hitl_reason += "Verifier requested human review"

    # User manually requested re-check
    if state.get("force_hitl"):
        hitl_required = True
        if hitl_reason:
            hitl_reason += "; "
        hitl_reason += "User requested re-check"

    return {
        "verification": verification.model_dump(),
        "hitl_required": hitl_required,
        "hitl_reason": hitl_reason
    }


def explainer_node(state: MathState):

    problem = state["parsed_problem"]["problem_text"]

    solution = state["solution"]

    explanation = explain_solution(problem, solution)

    return {"explanation": explanation}


# Build the LangGraph

builder = StateGraph(MathState)

builder.add_node("text_input", text_node)
builder.add_node("image_input", image_node)
builder.add_node("audio_input", audio_node)
builder.add_node("parser", parser_node)
builder.add_node("router", router_node)
builder.add_node("solver", solver_node)
builder.add_node("verifier", verifier_node)
builder.add_node("explainer", explainer_node)

builder.add_conditional_edges(
    START,
    input_router,
    {
        "text": "text_input",
        "image": "image_input",
        "audio": "audio_input"
    }
)

builder.add_edge("text_input", "parser")
builder.add_edge("image_input", "parser")
builder.add_edge("audio_input", "parser")
builder.add_edge("parser", "router")
builder.add_edge("router", "solver")
builder.add_edge("solver", "verifier")
builder.add_edge("verifier", "explainer")
builder.add_edge("explainer", END)

graph = builder.compile()


# TEST
# if __name__ == "__main__":

#     result = graph.invoke({
#         "input_type": "text",
#         "text_input": "Find derivative of x^2 + 3x"
#     })

#     print(result["solution"])
#     print(result["explanation"])