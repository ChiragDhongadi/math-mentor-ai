import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

def llm_invoke(prompt):

    response = llm.invoke(prompt)

    return response.content

# TESTING
# if __name__ == "__main__":

#     print(llm_invoke("What is 2+2?"))