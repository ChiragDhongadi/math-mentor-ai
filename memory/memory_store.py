import sqlite3
import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Always store DB in project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "math_memory.db")

print("Using memory DB:", DB_PATH)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    embedding BLOB,
    solution TEXT,
    verification TEXT
)
""")

conn.commit()


# ------------------------------
# Save Interaction
# ------------------------------
def store_memory(question, solution, verification):

    # Check if question already exists
    cursor.execute(
        "SELECT id FROM memory WHERE question=?",
        (question,)
    )

    existing = cursor.fetchone()

    if existing:
        # If this is a human correction/verification, update the existing entry
        if verification.get("corrected_by_human") or verification.get("human_verified"):
            print("Updating existing memory with human verified solution.")
            cursor.execute(
                "UPDATE memory SET solution=?, verification=? WHERE id=?",
                (solution, json.dumps(verification), existing[0])
            )
            conn.commit()
            return
        else:
            print("Question already stored in memory.")
            return

    embedding = model.encode(question).astype(np.float32).tobytes()

    cursor.execute(
        "INSERT INTO memory (question, embedding, solution, verification) VALUES (?, ?, ?, ?)",
        (question, embedding, solution, json.dumps(verification))
    )

    conn.commit()

    print("Stored new question in memory.")


# ------------------------------
# Retrieve Similar Problems
# ------------------------------
def retrieve_similar(question, k=3):

    query_embedding = model.encode(question).astype(np.float32)

    cursor.execute("SELECT question, embedding, solution, verification FROM memory")

    rows = cursor.fetchall()

    similarities = []

    for q, emb_blob, sol, ver_json in rows:

        emb = np.frombuffer(emb_blob, dtype=np.float32)

        score = np.dot(query_embedding, emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(emb)
        )

        print("Memory candidate:", q)
        print("Similarity score:", score)

        verification = {}
        if ver_json:
            try:
                verification = json.loads(ver_json)
            except:
                pass

        similarities.append((score, q, sol, verification))

    similarities.sort(key=lambda x: x[0], reverse=True)

    # Only accept strong matches
    threshold = 0.80
    filtered = [item for item in similarities if item[0] > threshold]

    return filtered[:k]