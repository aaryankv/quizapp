import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Backend API endpoints
USER_DETAILS_API = "http://127.0.0.1:5000/api/user-details"
QUESTIONS_API = "http://127.0.0.1:5000/api/generate-questions"
SUBMIT_QUIZ_API = "http://127.0.0.1:5000/api/submit-quiz"
SCORE_API = "http://127.0.0.1:5000/api/calculate-score"
CERTIFICATE_API = "http://127.0.0.1:5000/api/generate-certificate"

# Function to fetch questions based on user details
def fetch_questions(user_details):
    try:
        response = requests.post(USER_DETAILS_API, json=user_details)
        response.raise_for_status()
        user_id = response.json().get("user_id")
        questions_response = requests.get(f"{QUESTIONS_API}?user_id={user_id}")
        questions_response.raise_for_status()
        return questions_response.json().get("questions", []), user_id
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching questions: {e}")
        return [], None

# Function to submit the quiz answers
def submit_quiz(user_id, answers):
    try:
        response = requests.post(SUBMIT_QUIZ_API, json={"user_id": user_id, "answers": answers})
        response.raise_for_status()
        return True  # Successfully submitted the answers
    except requests.exceptions.RequestException as e:
        st.error(f"Error submitting quiz: {e}")
        return False

# Function to fetch the score after quiz submission
def fetch_score(user_id, domain):
    try:
        response = requests.post(SCORE_API, json={"user_id": user_id, "domain": domain})
        response.raise_for_status()
        score_data = response.json()
        return score_data.get("score"), score_data.get("total_questions_attempted")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching score: {e}")
        return None, None

# Function to fetch the generated certificate dynamically based on user ID
def fetch_certificate(user_id):
    try:
        # Call the certificate generation API
        response = requests.post(CERTIFICATE_API, json={"user_id": user_id})
        response.raise_for_status()

        # Get the certificate path from the API response
        certificate_path = response.json().get("certificate_path")

        if certificate_path:
            # Check if the path is a local file
            if certificate_path.startswith("C:") or certificate_path.startswith("/") or certificate_path.startswith("\\"):
                certificate_image = Image.open(certificate_path)
                return certificate_image
            else:
                # Fetch the image from a URL
                image_response = requests.get(certificate_path)
                image_response.raise_for_status()
                certificate_image = Image.open(BytesIO(image_response.content))
                return certificate_image
        else:
            st.error("Certificate generation failed. Please try again.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching certificate: {e}")
        return None
    except FileNotFoundError as e:
        st.error(f"Certificate file not found: {e}")
        return None


# Main app
def main():
    st.title("Quiz Application")

    # Sidebar navigation
    menu = st.sidebar.selectbox("Menu", ["User Details", "Quiz", "Results"])

    # State initialization
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "domain" not in st.session_state:
        st.session_state.domain = None

    if menu == "User Details":
        st.header("Enter Your Details")

        # User details form
        with st.form("user_details_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            contact_number = st.text_input("Contact Number")
            domain = "Engineering"
            submitted = st.form_submit_button("Submit")

            if submitted:
                if not name or not email or not contact_number or not domain:
                    st.error("Please fill in all fields.")
                else:
                    user_details = {
                        "name": name,
                        "email": email,
                        "contact_number": contact_number,
                        "domain": domain
                    }
                    questions, user_id = fetch_questions(user_details)
                    if questions:
                        st.session_state.questions = questions
                        st.session_state.user_id = user_id
                        st.session_state.current_question = 0
                        st.session_state.answers = {}
                        st.session_state.domain = domain
                        st.success("User details submitted successfully! Navigate to the Quiz tab.")

    elif menu == "Quiz":
        if not st.session_state.questions:
            st.warning("Please fill in your user details first in the 'User Details' tab.")
        else:
            questions = st.session_state.questions
            current_question_index = st.session_state.current_question

            # Safeguard to prevent out-of-bounds error
            if current_question_index < 0:
                st.session_state.current_question = 0
            elif current_question_index >= len(questions):
                st.session_state.current_question = len(questions) - 1

            # Display current question
            question = questions[st.session_state.current_question]
            st.header(f"Question {st.session_state.current_question + 1} of {len(questions)}")
            st.write(question["question"])

            # Display answer options
            options = [
                question["option_1"],
                question["option_2"],
                question["option_3"],
                question["option_4"]
            ]
            selected_option = st.radio(
                "Select an answer",
                options,
                key=f"question_{st.session_state.current_question}",
                index=options.index(st.session_state.answers.get(question["id"], options[0]))
                if question["id"] in st.session_state.answers else 0
            )

            # Save the selected option to session state
            st.session_state.answers[question["id"]] = selected_option

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Previous"):
                    if st.session_state.current_question > 0:
                        st.session_state.current_question -= 1

            with col2:
                if st.button("Next"):
                    if st.session_state.current_question < len(questions) - 1:
                        st.session_state.current_question += 1

            with col3:
                if st.button("Submit Quiz"):
                    if submit_quiz(st.session_state.user_id, st.session_state.answers):
                        st.success("Quiz submitted successfully! Navigate to the Results tab.")

    elif menu == "Results":
        if not st.session_state.answers:
            st.warning("Please complete the quiz in the 'Quiz' tab.")
        else:
            user_id = st.session_state.user_id
            domain = st.session_state.domain
            score, total_questions_attempted = fetch_score(user_id, domain)

            if score is not None:
                st.header("Quiz Results")
                st.write(f"Your Score: {score}")
                st.write(f"Total Questions Attempted: {total_questions_attempted}")
                st.success("Thank you for taking the quiz!")

                # Fetch and display the certificate
                certificate_image = fetch_certificate(user_id)
                if certificate_image:
                    st.header("Certificate of Achievement")
                    st.image(certificate_image, use_container_width=True)  # Updated parameter

if __name__ == "__main__":
    main()
