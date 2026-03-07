import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import tempfile
from pipeline.math_graph import graph
from multimodal.ocr import extract_text_from_image
from multimodal.audio import transcribe_audio
from memory.memory_store import store_memory

st.set_page_config(
    page_title="AI Math Mentor",
    page_icon="📘",
    layout="wide"
)

st.title("📘 AI Math Mentor")
st.caption("Multimodal JEE Math Solver using RAG + LangGraph Agents")

# Sidebar
st.sidebar.header("Input Mode")
mode = st.sidebar.radio(
    "Choose input type",
    ["Text", "Image", "Audio"],
    key="input_mode"
)

# Clear previous result when input mode changes
if "last_mode" not in st.session_state:
    st.session_state["last_mode"] = mode

if st.session_state["last_mode"] != mode:
    if "result" in st.session_state:
        del st.session_state["result"]

    st.session_state["last_mode"] = mode

user_input = None

# ----------------------
# TEXT INPUT
# ----------------------
if mode == "Text":

    st.subheader("✏️ Enter Math Question")

    user_input = st.text_area(
        "Type your math problem",
        placeholder="Example: Find derivative of x^2 + 3x"
    )

# ----------------------
# IMAGE INPUT
# ----------------------
elif mode == "Image":

    st.subheader("🖼 Upload Image")

    uploaded_image = st.file_uploader(
        "Upload JPG / PNG",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_image:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_image.read())
            image_path = tmp.name

        st.image(uploaded_image, caption="Uploaded Image")

        # Unpack text and confidence
        extracted_text, confidence = extract_text_from_image(image_path)

        st.subheader("OCR Extracted Text")

        user_input = st.text_area(
            "Edit extracted text if needed",
            value=extracted_text
        )

# ----------------------
# AUDIO INPUT
# ----------------------
elif mode == "Audio":

    st.subheader("🎤 Upload Audio")

    uploaded_audio = st.file_uploader(
        "Upload audio file",
        type=["wav", "mp3"]
    )

    if uploaded_audio:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_audio.read())
            audio_path = tmp.name

        st.audio(uploaded_audio)

        # Unpack text and confidence
        transcript, confidence = transcribe_audio(audio_path)

        st.subheader("Audio Transcript")

        user_input = st.text_area(
            "Edit transcript if needed",
            value=transcript
        )

# ----------------------
# SOLVE BUTTON
# ----------------------

if st.button("Solve Problem", type="primary"):

    if not user_input:
        st.warning("Please provide a question.")
        st.stop()

    with st.spinner("Running AI Agents..."):

        if mode == "Text":

            st.session_state["result"] = graph.invoke({
                "input_type": "text",
                "text_input": user_input,
                "force_hitl": st.session_state.get("force_hitl", False)
            })

        elif mode == "Image":

            st.session_state["result"] = graph.invoke({
                "input_type": "image",
                "image_path": image_path,
                "force_hitl": st.session_state.get("force_hitl", False)
            })

        elif mode == "Audio":

            st.session_state["result"] = graph.invoke({
                "input_type": "audio",
                "audio_path": audio_path,
                "force_hitl": st.session_state.get("force_hitl", False)
            })
    st.session_state["force_hitl"] = False

# ----------------------
# SHOW RESULT (important)
# ----------------------

if "result" in st.session_state:

    result = st.session_state["result"]

    st.success("Solution Generated")

    col1, col2 = st.columns([2, 1])

    # LEFT PANEL
    with col1:

        st.subheader("Final Answer")

        solution = result["solution"]

        import re, json

        try:
            data = json.loads(solution)
            solution = data["solution"]
        except:
            match = re.search(r'"solution"\s*:\s*"([^"]+)"', solution)
            if match:
                solution = match.group(1)

        st.markdown(f"### {solution}")

        st.subheader("Step-by-Step Explanation")
        st.write(result["explanation"])

        # Initialize edited_solution with the parsed solution by default
        # This ensures it exists for the Feedback section even if HITL is skipped
        edited_solution = solution

        # ----------------------
        # HUMAN IN LOOP
        # ----------------------

        if result.get("hitl_required"):

            st.warning("⚠ Human Review Required")

            st.write("Reason:", result.get("hitl_reason"))

            edited_solution = st.text_input(
                "Edit the solution if needed",
                value=solution
            )

            hitl_col1, hitl_col2, hitl_col3 = st.columns(3)

            with hitl_col1:

                if st.button("Approve"):

                    store_memory(
                        result["parsed_problem"]["problem_text"],
                        edited_solution,
                        result.get("verification", {})
                    )

                    st.success("Solution approved and stored.")
                    st.session_state["result"]["hitl_required"] = False
                    st.session_state["result"]["solution"] = edited_solution
                    st.rerun()

            with hitl_col2:

                if st.button("Edit & Save"):

                    store_memory(
                        result["parsed_problem"]["problem_text"],
                        edited_solution,
                        {"corrected_by_human": True}
                    )

                    st.success("Human correction saved.")
                    st.session_state["result"]["hitl_required"] = False
                    st.session_state["result"]["solution"] = edited_solution
                    st.rerun()

            with hitl_col3:

                if st.button("Reject"):

                    st.error("Solution rejected.")
                    # Clear the result so the user can try again
                    del st.session_state["result"]
                    st.rerun()
    

    # RIGHT PANEL
    with col2:

        st.subheader("Agent Trace")

        st.write(
            [
                "Parser Agent",
                "Intent Router",
                "Solver Agent",
                "Verifier Agent",
                "Explainer Agent"
            ]
        )

        st.subheader("Confidence")

        if "verification" in result:
            confidence = result["verification"].get("confidence", 0.9)
            st.progress(confidence)

        if result.get("memory_used"):
            st.success("Memory reused for similar problem")

    # ----------------------
    # RETRIEVED CONTEXT PANEL
    # ----------------------

    with st.expander("Retrieved Knowledge Context"):

        contexts = result.get("retrieved_context", [])

        if contexts:
            for i, chunk in enumerate(contexts, 1):
                st.markdown(f"**Source {i}**")
                st.write(chunk)
                st.divider()
        else:
            st.write("No knowledge retrieved.")

    # ----------------------
    # FEEDBACK
    # ----------------------

    st.subheader("Feedback")

    col1, col2, col3 = st.columns(3)

    # -----------------------
    # Correct Button
    # -----------------------
    with col1:
        if st.button("Correct"):

            result = st.session_state.get("result")

            if result:
                store_memory(
                    result["parsed_problem"]["problem_text"],
                    edited_solution,
                    {"human_verified": True}
                )

                st.success("Stored in memory!")

    # -----------------------
    # Incorrect Feedback
    # -----------------------
    with col2:
        feedback = st.text_input("Incorrect? Tell us why")

        if feedback:

            result = st.session_state.get("result")

            store_memory(
                result["parsed_problem"]["problem_text"],
                result["solution"],
                {"user_feedback": feedback}
            )

            # Trigger HITL
            st.session_state["force_hitl"] = True

            st.warning("Feedback stored. Human review triggered.")

            # rerun app so HITL block appears
            st.rerun()

    # -----------------------
    # Request Human Recheck
    # -----------------------
    with col3:
        if st.button("Request Human Re-Check"):

            st.session_state["force_hitl"] = True
            
            # Force the UI to show the HITL box immediately for the current result
            st.session_state["result"]["hitl_required"] = True
            st.session_state["result"]["hitl_reason"] = "User requested re-check"
            st.rerun()