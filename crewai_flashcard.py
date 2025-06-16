# crewai_flashcard.py

import os
from crewai import Agent, Task, Crew
from crewai_tools import PDFSearchTool
import openai
from ast import literal_eval

# Set your OpenAI model
#os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'  # or use 'gpt-4o-mini'
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the PDFSearchTool (without a preset PDF)
pdf_tool = PDFSearchTool()

# Agent 1: PDF Extractor Agent – extracts full text from the PDF.
pdf_extractor = Agent(
    role="PDF Extractor",
    goal="Extract the full text content from the provided PDF.",
    backstory="You specialize in reading and processing PDFs to return useful study content.",
    verbose=True,
    tools=[pdf_tool]
)

# Agent 2: Flashcard Generator Agent – generates flashcards based on the extracted text.
flashcard_generator = Agent(
    role="Flashcard Generator",
    goal="Generate flashcards with questions and answers based on the extracted text.",
    backstory="You create study flashcards to test understanding, ensuring each flashcard has a clear question and answer.",
    verbose=True
)

# Task 1: Extraction Task – Extract full text from the PDF.
extraction_task = Task(
    description=(
        "Extract and return the full text content from the PDF located at {pdf_file_path}."
    ),
    expected_output="A string containing the extracted text from the PDF.",
    agent=pdf_extractor
)

# Task 2: Flashcard Generation Task – Generate {flashcard_count} flashcards.
flashcard_task = Task(
    description=(
        "Based on the following extracted text:"
        "Generate {flashcard_count} flashcards. Each flashcard should have a question and a corresponding answer. "
        "Return the flashcards as a Python dictionary where each key is a flashcard question and its corresponding value is the answer."
    ),
    expected_output="A Python dictionary of flashcards.",
    output_file="flashcards.json",
    agent=flashcard_generator,
    context=[extraction_task]
)

# Assemble the Crew
flashcard_crew = Crew(
    agents=[pdf_extractor, flashcard_generator],
    tasks=[extraction_task, flashcard_task],
    verbose=True
)

def generate_flashcards(pdf_file_path: str, flashcard_count: int) -> str:
    """
    Runs the CrewAI flashcard generator to produce flashcards from the given PDF.
    
    Args:
        pdf_file_path (str): Path to the PDF file.
        flashcard_count (int): Number of flashcards to generate.
        
    Returns:
        str: A string representation of a Python dictionary containing the flashcards.
    """
    inputs = {
        "pdf_file_path": pdf_file_path,
        "flashcard_count": flashcard_count
    }
    results = flashcard_crew.kickoff(inputs=inputs)
    # Return the raw output (a string) from the flashcard task.
    output = results.raw.strip()
    return output

if __name__ == "__main__":
    # For testing purposes
    pdf_path = "sample.pdf"  # Replace with a valid PDF file path
    flashcard_count = 3
    flashcards_str = generate_flashcards(pdf_path, flashcard_count)
    try:
        flashcards = literal_eval(flashcards_str)
        print("Generated Flashcards:")
        for question, answer in flashcards.items():
            print("Q:", question)
            print("A:", answer)
    except Exception as e:
        print("Error parsing flashcards:", e)
