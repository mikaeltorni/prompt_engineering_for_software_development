"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_welcome(): Displays welcome message
    display_question(question_data: dict): Displays a single question
    validate_answer(user_input: str, valid_options: list) -> bool: Validates user input
    play_quiz() -> None: Main game loop
    display_results(score: int, total_questions: int) -> None: Shows final results

Command Line Usage Example:
    python quiz_game.py
"""

import random
import logging
import time
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Quiz questions database
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct_answer": "B"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "B"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
        "correct_answer": "B"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct_answer": "B"
    }
]

def display_welcome() -> None:
    """
    Displays the welcome message and game instructions.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Displaying welcome message")
    print("\n=== Welcome to the Python Quiz Game! ===")
    print("Answer each question by entering the letter of your choice (A, B, C, or D)")
    print("Let's begin!\n")

def display_question(question_data: Dict) -> None:
    """
    Displays a single question with its multiple choice options.

    Parameters:
        question_data (dict): Dictionary containing question information

    Returns:
        None
    """
    logger.debug(f"Displaying question: {question_data['question']}")
    print("\n" + question_data["question"])
    for i, option in enumerate(question_data["options"]):
        print(f"{chr(65 + i)}. {option}")

def validate_answer(user_input: str, valid_options: List[str]) -> bool:
    """
    Validates if the user input is a valid option.

    Parameters:
        user_input (str): The user's input
        valid_options (list): List of valid answer options

    Returns:
        bool: True if input is valid, False otherwise
    """
    logger.debug(f"Validating answer: {user_input}")
    return user_input.upper() in valid_options

def play_quiz() -> None:
    """
    Main game loop that handles the quiz logic.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting new quiz game")
    score = 0
    questions = QUIZ_QUESTIONS.copy()
    random.shuffle(questions)
    total_questions = len(questions)

    display_welcome()

    for i, question in enumerate(questions, 1):
        display_question(question)
        
        while True:
            user_answer = input("\nYour answer (A/B/C/D): ").upper()
            if validate_answer(user_answer, ['A', 'B', 'C', 'D']):
                break
            print("Invalid input! Please enter A, B, C, or D.")

        if user_answer == question["correct_answer"]:
            print("Correct! 🎉")
            score += 1
        else:
            correct_option = question["options"][ord(question["correct_answer"]) - 65]
            print(f"Sorry, that's incorrect. The correct answer was: {correct_option}")

        print(f"Current score: {score}/{i}")
        time.sleep(1)

    display_results(score, total_questions)

def display_results(score: int, total_questions: int) -> None:
    """
    Displays the final quiz results.

    Parameters:
        score (int): Final score
        total_questions (int): Total number of questions

    Returns:
        None
    """
    logger.info(f"Game finished. Final score: {score}/{total_questions}")
    percentage = (score / total_questions) * 100
    print("\n=== Quiz Complete! ===")
    print(f"Final Score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%")

    if percentage == 100:
        print("Perfect score! Outstanding! 🏆")
    elif percentage >= 80:
        print("Great job! 🌟")
    elif percentage >= 60:
        print("Good effort! 👍")
    else:
        print("Keep practicing! 📚")

def main() -> None:
    """
    Main function to run the quiz game with replay option.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        play_quiz()
        
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").lower()
            if play_again in ['yes', 'no']:
                break
            print("Please enter 'yes' or 'no'.")

        if play_again != 'yes':
            print("\nThanks for playing! Goodbye! 👋")
            break

if __name__ == "__main__":
    main()