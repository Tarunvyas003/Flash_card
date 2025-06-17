import streamlit as st
from PyPDF2 import PdfReader
import openai
import ast

# ✅ Set your new OpenAI API Key (for testing only)
openai.api_key = "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"

# ---------------------------
def extract_text(uploaded_file):
    uploaded_file.seek(0)
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

# ---------------------------
def generate_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an educational assistant."},
            {"role": "user", "content": f"Summarize this document:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

# ---------------------------
def generate_flashcards(text, num_cards=5):
    prompt = (
        f"Create {num_cards} flashcards based on the following document:\n\n{text}\n\n"
        "Return them as a Python dictionary in the format {'Question': 'Answer'}."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful tutor."},
            {"role": "user", "content": prompt}
        ]
    )
    output = response.choices[0].message.content.strip()
    try:
        flashcards = ast.literal_eval(output)
        return flashcards if isinstance(flashcards, dict) else {}
    except:
        return {}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Flashcard Generator")
st.title("📚 AI Flashcard Generator")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully.")
    raw_text = extract_text(uploaded_file)

    if raw_text:
        st.subheader("Document Summary")
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = generate_summary(raw_text)
                st.text_area("Summary", summary, height=200)

        st.subheader("Flashcards")
        num = st.slider("Number of Flashcards", 1, 20, 5)
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                cards = generate_flashcards(raw_text, num)
                for q, a in cards.items():
                    st.markdown(f"**Q:** {q}\n\n**A:** {a}")






# # Import the CrewAI flashcard module (modified below to remove page range)
# from crewai_flashcard import generate_flashcards

# # ---------------------------
# # Helper Function: Extract text from PDF
# # ---------------------------
# def extract_text(uploaded_file):
#     # Ensure file size is less than 10MB
#     uploaded_file.seek(0, os.SEEK_END)
#     if uploaded_file.tell() > 10 * 1024 * 1024:
#         st.error("File exceeds 10MB limit.")
#         return ""
#     uploaded_file.seek(0)
#     pdf_reader = PdfReader(uploaded_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"
#     return text

# # ---------------------------
# # OpenAI Response Functions
# # ---------------------------
# def generate_summary_from_text(text):
#     prompt = (
#         f"Summarize the following document in a concise manner, highlighting the key points that a student should know:\n\n{text}"
#     )
#     messages = [
#         {"role": "system", "content": "You are an educational assistant."},
#         {"role": "user", "content": prompt}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# def chat_with_document(text, conversation_history, user_query):
#     messages = conversation_history + [
#         {"role": "user", "content": f"Based on the following document:\n\n{text}\n\nQuestion: {user_query}"}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# def generate_questions_from_text(text, num_questions):
#     prompt = (
#         f"Generate {num_questions} study questions with answers based on the following document. "
#         "Return the output as a table in CSV format with two columns: 'Question' and 'Answer'.\n\nDocument:\n\n{text}"
#     )
#     messages = [
#         {"role": "system", "content": "You are an educational assistant that generates study questions."},
#         {"role": "user", "content": prompt}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     # Expecting CSV output (with header: Question,Answer)
#     return completion.choices[0].message.content.strip()

# # ---------------------------
# # Sidebar: File Upload & Mode Selection
# # ---------------------------
# st.sidebar.title("Study Companion Setup")

# uploaded_pdf = st.sidebar.file_uploader("Upload your study PDF (max 10MB)", type="pdf")
# mode = st.sidebar.radio("Select Mode", ("Chat", "Test Your Knowledge", "Flashcards"))

# # For Test Your Knowledge: number of questions (max 50)
# num_questions = None
# if mode == "Test Your Knowledge":
#     num_questions = st.sidebar.number_input("Number of questions to generate (max 50):", min_value=1, max_value=50, value=10, step=1)
#     if st.sidebar.button("Generate Questions"):
#         st.session_state.gen_questions = True

# # For Flashcards: number of flashcards (max 5)
# num_flashcards = None
# if mode == "Flashcards":
#     num_flashcards = st.sidebar.number_input("Number of flashcards to generate (max 5):", min_value=1, max_value=5, value=3, step=1)
#     if st.sidebar.button("Generate Flashcards"):
#         st.session_state.gen_flashcards = True

# # ---------------------------
# # Session State Initialization
# # ---------------------------
# if "pdf_text" not in st.session_state:
#     st.session_state.pdf_text = None
# if "summary" not in st.session_state:
#     st.session_state.summary = None
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = [{"role": "assistant", "content": "Hi, how can I help you with your study material?"}]
# if "questions_table" not in st.session_state:
#     st.session_state.questions_table = None
# if "flashcards" not in st.session_state:
#     st.session_state.flashcards = {}
# if "current_card" not in st.session_state:
#     st.session_state.current_card = 0
# if "score" not in st.session_state:
#     st.session_state.score = 0
# if "show_answer" not in st.session_state:
#     st.session_state.show_answer = False

# # ---------------------------
# # Process PDF Upload
# # ---------------------------
# if uploaded_pdf is not None:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(uploaded_pdf.read())
#         st.session_state.pdf_file_path = tmp.name
#     st.session_state.pdf_text = extract_text(uploaded_pdf)
#     if st.session_state.pdf_text:
#         st.sidebar.success("PDF uploaded and processed successfully!")
#     else:
#         st.sidebar.error("Failed to extract text from the PDF.")

# # ---------------------------
# # Main Area: Mode-Based Display (using side menu)
# # ---------------------------
# st.title("Study Companion: PDF-based Learning")

# if st.session_state.pdf_text is None:
#     st.info("Please upload a PDF from the sidebar to begin.")
# else:
#     if mode == "Chat":
#         st.header("Chat with Your Study Companion")
#         for msg in st.session_state.chat_history:
#             st.chat_message(msg["role"]).write(msg["content"])
#         user_question = st.chat_input("Ask a question about the document:")
#         if user_question:
#             st.session_state.chat_history.append({"role": "user", "content": user_question})
#             st.chat_message("user").write(user_question)
#             with st.spinner("Processing your question..."):
#                 response = chat_with_document(st.session_state.pdf_text, st.session_state.chat_history, user_question)
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#             st.chat_message("assistant").write(response)

#     elif mode == "Test Your Knowledge":
#         st.header("Test Your Knowledge")
#         if num_questions is None or not st.session_state.get("gen_questions", False):
#             st.info("Enter the number of questions and press 'Generate Questions' from the sidebar.")
#         else:
#             with st.spinner("Generating questions..."):
#                 questions_csv = generate_questions_from_text(st.session_state.pdf_text, num_questions)
#             # Convert CSV output into a table (assuming header row "Question,Answer")
#             try:
#                 lines = questions_csv.splitlines()
#                 if len(lines) < 2:
#                     st.error("Failed to generate questions properly.")
#                 else:
#                     header = lines[0].split(",")
#                     data = [line.split(",") for line in lines[1:]]
#                     st.table(data, headers=header)
#                     st.session_state.questions_table = data
#             except Exception as e:
#                 st.error(f"Error processing questions: {e}")

#     elif mode == "Flashcards":
#         st.header("Practice Flashcards")
#         if not st.session_state.get("gen_flashcards", False):
#             st.info("Enter the number of flashcards and press 'Generate Flashcards' from the sidebar.")
#         else:
#             if st.button("Reset Flashcards"):
#                 st.session_state.flashcards = {}
#                 st.session_state.current_card = 0
#                 st.session_state.score = 0
#                 st.session_state.show_answer = False
#                 st.session_state.gen_flashcards = False
#             if st.session_state.get("gen_flashcards", False):
#                 # Generate flashcards using the CrewAI module (which returns a Python dictionary)
#                 flashcards = generate_flashcards(st.session_state.pdf_file_path, num_flashcards)
#                 st.session_state.flashcards = flashcards
#                 st.session_state.current_card = 0
#                 st.session_state.score = 0
#                 st.session_state.show_answer = False
#                 st.success("Flashcards generated successfully!")
#                 st.session_state.gen_flashcards = False  # reset flag after generation
            
#             if not st.session_state.flashcards:
#                 st.info("No flashcards available. Click the 'Generate Flashcards' button in the sidebar.")
#             else:
#                 total_cards = len(st.session_state.flashcards)
#                 if st.session_state.current_card >= total_cards:
#                     st.success(f"You've completed all flashcards! Final Score: {st.session_state.score} / {total_cards}")
#                     st.info("Restart the session or generate new flashcards from the sidebar.")
#                 else:
#                     flashcards = st.session_state.flashcards
#                     current_keys = list(flashcards.keys())
#                     current_question = current_keys[st.session_state.current_card]
#                     current_answer = flashcards[current_question]
#                     st.write(f"**Question:** {current_question}")
#                     if st.button("Show Answer"):
#                         st.session_state.show_answer = True
#                     if st.session_state.show_answer:
#                         st.write(f"**Answer:** {current_answer}")
#                         col1, col2 = st.columns(2)
#                         with col1:
#                             if st.button("Correct"):
#                                 st.session_state.score += 1
#                                 st.success("Correct!")
#                         with col2:
#                             if st.button("Wrong"):
#                                 st.error("Incorrect!")
#                         if st.button("Next Card"):
#                             st.session_state.current_card += 1
#                             st.session_state.show_answer = False
#                             st.rerun()
#                     st.write(f"**Current Score:** {st.session_state.score} / {total_cards}")




######################################################################################################


# # ---------------------------
# # Helper Function: Extract text from PDF
# # ---------------------------
# def extract_text(uploaded_file):
#     pdf_reader = PdfReader(uploaded_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text
#     return text

# # ---------------------------
# # OpenAI Response Functions (using new style)
# # ---------------------------
# def generate_summary_from_text(text):
#     prompt = (
#         f"Summarize the following document in a concise manner, "
#         "highlighting the key points that a student should know:\n\n{text}"
#     )
#     messages = [
#         {"role": "system", "content": "You are an educational assistant."},
#         {"role": "user", "content": prompt}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# def chat_with_document(text, conversation_history, user_query):
#     messages = conversation_history + [
#         {"role": "user", "content": f"Based on the following document:\n\n{text}\n\nQuestion: {user_query}"}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# def generate_flashcards_from_text(text, num_cards):
#     prompt = (
#         f"Generate {num_cards} flashcards based on the following document. \n\nDocument:\n\n{text} "
#         "Return a Python dictionary where each key is a flashcard question and its corresponding value is the answer. "
#         #"Do not include any additional text.\n\nDocument:\n\n{text}"
#     )
#     messages = [
#         {"role": "system", "content": "You are an educational assistant that creates study flashcards."},
#         {"role": "user", "content": prompt}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     output = completion.choices[0].message.content.strip()
#     try:
#         # Use literal_eval to safely evaluate the string as a Python dictionary.
#         flashcards = literal_eval(output)
#         if isinstance(flashcards, dict):
#             return flashcards
#         else:
#             return {}
#     except Exception as e:
#         st.error(f"Error parsing flashcards: {e}")
#         return {}

# # ---------------------------
# # Sidebar: File Upload & Mode Selection
# # ---------------------------
# st.sidebar.title("Study Companion Setup")

# uploaded_pdf = st.sidebar.file_uploader("Upload your study PDF", type="pdf")
# mode = st.sidebar.radio("Select Mode", ("Summary", "Chat", "Flashcards"))

# num_flashcards = None
# if mode == "Flashcards":
#     num_flashcards = st.sidebar.number_input("Number of flashcards to generate:", min_value=1, max_value=20, value=5, step=1)

# # ---------------------------
# # Session State Initialization
# # ---------------------------
# if "pdf_text" not in st.session_state:
#     st.session_state.pdf_text = None
# if "summary" not in st.session_state:
#     st.session_state.summary = None
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = [{"role": "assistant", "content": "Hi, how can I help you with your study material?"}]
# if "flashcards" not in st.session_state:
#     st.session_state.flashcards = {}
# if "current_card" not in st.session_state:
#     st.session_state.current_card = 0
# if "score" not in st.session_state:
#     st.session_state.score = 0
# if "show_answer" not in st.session_state:
#     st.session_state.show_answer = False

# # ---------------------------
# # Process PDF Upload
# # ---------------------------
# if uploaded_pdf is not None:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(uploaded_pdf.read())
#         st.session_state.pdf_file_path = tmp.name
#     st.session_state.pdf_text = extract_text(uploaded_pdf)
#     st.sidebar.success("PDF uploaded and processed successfully!")

# # ---------------------------
# # Main Area: Mode-Based Display
# # ---------------------------
# st.title("Study Companion: PDF-based Learning")

# if st.session_state.pdf_text is None:
#     st.info("Please upload a PDF from the sidebar to begin.")
# else:
#     if mode == "Summary":
#         st.header("Summary & Key Points")
#         if st.session_state.summary is None:
#             with st.spinner("Generating summary..."):
#                 st.session_state.summary = generate_summary_from_text(st.session_state.pdf_text)
#         st.write(st.session_state.summary)

#     elif mode == "Chat":
#         st.header("Chat with Your Study Companion")
#         for msg in st.session_state.chat_history:
#             st.chat_message(msg["role"]).write(msg["content"])
#         user_question = st.chat_input("Ask a question about the document:")
#         if user_question:
#             st.session_state.chat_history.append({"role": "user", "content": user_question})
#             st.chat_message("user").write(user_question)
#             with st.spinner("Processing your question..."):
#                 response = chat_with_document(st.session_state.pdf_text, st.session_state.chat_history, user_question)
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#             st.chat_message("assistant").write(response)

#     elif mode == "Flashcards":
#         st.header("Practice Flashcards")
#         if st.button("Generate Flashcards"):
#             with st.spinner("Generating flashcards..."):
#                 flashcards = generate_flashcards_from_text(st.session_state.pdf_text, num_flashcards)
#             st.session_state.flashcards = flashcards
#             st.session_state.current_card = 0
#             st.session_state.score = 0
#             st.session_state.show_answer = False
#             st.success("Flashcards generated successfully!")
        
#         if not st.session_state.flashcards:
#             st.info("No flashcards available. Click the button above to generate flashcards.")
#         else:
#             total_cards = len(st.session_state.flashcards)
#             if st.session_state.current_card >= total_cards:
#                 st.success(f"You've completed all flashcards! Final Score: {st.session_state.score} / {total_cards}")
#                 st.info("Restart the session or generate new flashcards from the sidebar.")
#             else:
#                 flashcards = st.session_state.flashcards
#                 current_keys = list(flashcards.keys())
#                 current_question = current_keys[st.session_state.current_card]
#                 current_answer = flashcards[current_question]
#                 st.write(f"**Question:** {current_question}")
#                 if st.button("Show Answer"):
#                     st.session_state.show_answer = True
#                 if st.session_state.show_answer:
#                     st.write(f"**Answer:** {current_answer}")
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if st.button("Correct"):
#                             st.session_state.score += 1
#                             st.success("Correct!")
#                     with col2:
#                         if st.button("Wrong"):
#                             st.error("Incorrect!")
#                     if st.button("Next Card"):
#                         st.session_state.current_card += 1
#                         st.session_state.show_answer = False
#                         st.rerun()
#                 st.write(f"**Current Score:** {st.session_state.score} / {total_cards}")




# # ---------------------------
# # Helper Function: Extract text from PDF
# # ---------------------------
# def extract_text(uploaded_file):
#     pdf_reader = PdfReader(uploaded_file)
#     text = ""
#     for page in pdf_reader.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text
#     return text

# # ---------------------------
# # OpenAI Response Functions (using new style)
# # ---------------------------
# def generate_summary_from_text(text):
#     prompt = (
#         f"Summarize the following document in a concise manner, "
#         "highlighting the key points that a student should know:\n\n{text}"
#     )
#     messages = [
#         {"role": "system", "content": "You are an educational assistant."},
#         {"role": "user", "content": prompt}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# def chat_with_document(text, conversation_history, user_query):
#     # Build a message list that includes the conversation history plus the new query with context.
#     messages = conversation_history + [
#         {"role": "user", "content": f"Based on the following document:\n\n{text}\n\nQuestion: {user_query}"}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     return completion.choices[0].message.content.strip()

# def generate_flashcards_from_text(text, num_cards):
#     prompt = (
#         f"Generate {num_cards} flashcards based on the following document. "
#         "Return a Python dictionary (in valid JSON format) where each key is a flashcard question and its value is the corresponding answer. "
#         f"Document:\n\n{text}"
#     )
#     messages = [
#         {"role": "system", "content": "You are an educational assistant that creates study flashcards."},
#         {"role": "user", "content": prompt}
#     ]
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=messages
#     )
#     output = completion.choices[0].message.content.strip()
#     try:
#         flashcards = json.loads(output)
#         if isinstance(flashcards, dict):
#             return flashcards
#         else:
#             return {}
#     except Exception as e:
#         st.error(f"Error parsing flashcards: {e}")
#         return {}

# # ---------------------------
# # Sidebar: File Upload & Mode Selection
# # ---------------------------
# st.sidebar.title("Study Companion Setup")

# uploaded_pdf = st.sidebar.file_uploader("Upload your study PDF", type="pdf")
# mode = st.sidebar.radio("Select Mode", ("Summary", "Chat", "Flashcards"))

# # For Flashcards, allow user to input number of flashcards
# num_flashcards = None
# if mode == "Flashcards":
#     num_flashcards = st.sidebar.number_input("Number of flashcards to generate:", min_value=1, max_value=20, value=5, step=1)

# # ---------------------------
# # Session State Initialization
# # ---------------------------
# if "pdf_text" not in st.session_state:
#     st.session_state.pdf_text = None
# if "summary" not in st.session_state:
#     st.session_state.summary = None
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = [{"role": "assistant", "content": "Hi, how can I help you with your study material?"}]
# if "flashcards" not in st.session_state:
#     st.session_state.flashcards = {}
# if "current_card" not in st.session_state:
#     st.session_state.current_card = 0
# if "score" not in st.session_state:
#     st.session_state.score = 0
# if "show_answer" not in st.session_state:
#     st.session_state.show_answer = False

# # ---------------------------
# # Process PDF Upload
# # ---------------------------
# if uploaded_pdf is not None:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(uploaded_pdf.read())
#         pdf_file_path = tmp.name
#     # Extract text from the PDF (all pages)
#     st.session_state.pdf_text = extract_text(pdf_file_path)
#     st.sidebar.success("PDF uploaded and processed successfully!")

# # ---------------------------
# # Main Area: Mode-Based Display
# # ---------------------------
# st.title("Study Companion: PDF-based Learning")

# if st.session_state.pdf_text is None:
#     st.info("Please upload a PDF from the sidebar to begin.")
# else:
#     if mode == "Summary":
#         st.header("Summary & Key Points")
#         if st.session_state.summary is None:
#             with st.spinner("Generating summary..."):
#                 st.session_state.summary = generate_summary_from_text(st.session_state.pdf_text)
#         st.write(st.session_state.summary)

#     elif mode == "Chat":
#         st.header("Chat with Your Study Companion")
#         # Display persistent chat history
#         for msg in st.session_state.chat_history:
#             st.chat_message(msg["role"]).write(msg["content"])
#         user_question = st.chat_input("Ask a question about the document:")
#         if user_question:
#             st.session_state.chat_history.append({"role": "user", "content": user_question})
#             st.chat_message("user").write(user_question)
#             with st.spinner("Processing your question..."):
#                 response = chat_with_document(st.session_state.pdf_text, st.session_state.chat_history, user_question)
#             st.session_state.chat_history.append({"role": "assistant", "content": response})
#             st.chat_message("assistant").write(response)

#     elif mode == "Flashcards":
#         st.header("Practice Flashcards")
#         # Provide a button to generate flashcards on demand.
#         if st.button("Generate Flashcards"):
#             with st.spinner("Generating flashcards..."):
#                 flashcards = generate_flashcards_from_text(st.session_state.pdf_text, num_flashcards)
#             st.session_state.flashcards = flashcards
#             st.session_state.current_card = 0
#             st.session_state.score = 0
#             st.session_state.show_answer = False
#             st.success("Flashcards generated successfully!")
        
#         if not st.session_state.flashcards:
#             st.info("No flashcards available. Click the button above to generate flashcards.")
#         else:
#             total_cards = len(st.session_state.flashcards)
#             if st.session_state.current_card >= total_cards:
#                 st.success(f"You've completed all flashcards! Final Score: {st.session_state.score} / {total_cards}")
#                 st.info("Restart the session or generate new flashcards from the sidebar.")
#             else:
#                 flashcards = st.session_state.flashcards
#                 # Get the current flashcard key-value pair.
#                 current_keys = list(flashcards.keys())
#                 current_key = current_keys[st.session_state.current_card]
#                 current_answer = flashcards[current_key]
#                 st.write(f"**Question:** {current_key}")
#                 if st.button("Show Answer"):
#                     st.session_state.show_answer = True
#                 if st.session_state.show_answer:
#                     st.write(f"**Answer:** {current_answer}")
#                     col1, col2 = st.columns(2)
#                     with col1:
#                         if st.button("Correct"):
#                             st.session_state.score += 1
#                             st.success("Correct!")
#                     with col2:
#                         if st.button("Wrong"):
#                             st.error("Incorrect!")
#                     if st.button("Next Card"):
#                         st.session_state.current_card += 1
#                         st.session_state.show_answer = False
#                         st.rerun()
#                 st.write(f"**Current Score:** {st.session_state.score} / {total_cards}")
