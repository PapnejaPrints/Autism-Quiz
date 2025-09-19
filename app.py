import json
import streamlit as st

# Load quiz data
def load_quiz(filename="quiz.json"):
    with open(filename, "r") as file:
        return json.load(file)

# Calculate score & interpretation
def calculate_score(answers, quiz):
    total = sum(answers.values())
    for rng, meaning in quiz["scale"]["interpretation"].items():
        low, high = map(int, rng.split("-"))
        if low <= total <= high:
            return total, meaning
    return total, "No interpretation available"

def restart_quiz():
    st.session_state.current_q = 0
    st.session_state.answers = {}
    # Reset all question-specific radio button states
    for key in list(st.session_state.keys()):
        if key.startswith("q"):
            del st.session_state[key]
    st.rerun()

def main():
    quiz = load_quiz()

    # Initialize session state
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    num_questions = len(quiz["questions"])
    q_index = st.session_state.current_q
    question = quiz["questions"][q_index]

    # Title + instructions
    st.title(quiz["quizTitle"])
    st.write(quiz["instructions"])
    st.markdown("---")

    # Progress bar
    answered_count = len(st.session_state.answers)
    st.progress(answered_count / num_questions)
    st.write(f"Progress: {answered_count}/{num_questions} answered")

    # Show current question
    st.subheader(f"Q{question['id']}: {question['text']}")
    choice = st.radio(
        "Select an option:",
        options=[opt["label"] for opt in quiz["scale"]["options"]],
        key=f"q{question['id']}",
        index=None
    )

    # Save answer
    if choice:
        value = next(opt["value"] for opt in quiz["scale"]["options"] if opt["label"] == choice)
        st.session_state.answers[q_index] = value

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", disabled=(q_index == 0)):
            st.session_state.current_q -= 1
            st.rerun()

    with col2:
        if st.button("Next ➡️", disabled=(q_index == num_questions - 1)):
            st.session_state.current_q += 1
            st.rerun()

    # Submit button on last question
    if q_index == num_questions - 1:
        if st.button("✅ Submit"):
            if len(st.session_state.answers) < num_questions:
                st.warning("⚠️ Please answer all questions before submitting!")
            else:
                score, result = calculate_score(st.session_state.answers, quiz)
                st.success(f"### Your Results\n**Score:** {score}\n\n**Vibe Category:** {result}")
                st.button("🔄 Restart Quiz", on_click=restart_quiz)

    # Footer credit line
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size:14px; color:gray;'>"
        "Brahmleen Papneja – Queen's University – Faculty of Health Sciences"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
