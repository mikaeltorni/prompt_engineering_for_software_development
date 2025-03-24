"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_welcome(): Display welcome message
    display_question(question: dict) -> None: Display a single question and its options
    get_valid_answer(max_options: int) -> str: Get and validate user input
    play_quiz() -> None: Main game loop
    calculate_percentage(score: int, total_possible: int) -> float: Calculate score percentage
    display_final_score(score: int, total_possible: int) -> None: Display final score

Command Line Usage Example:
    python quiz_game.py
"""

import random
import time
import logging
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
        "correct_answer": "3",  # Paris
        "points": 1
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct_answer": "2",  # Mars
        "points": 1
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "2",  # 4
        "points": 1
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
        "correct_answer": "2",  # Da Vinci
        "points": 1
    }
]

def display_welcome() -> None:
    """
    Display welcome message and game instructions.

    Parameters:
        None

    Returns:
        None
    """
    print("\n=== Welcome to the Quiz Game! ===")
    print("Answer the following multiple-choice questions.")
    print("Choose the number corresponding to your answer.")
    print("Good luck!\n")
    logger.debug("Welcome message displayed")

def display_question(question: dict) -> None:
    """
    Display a single question and its options.

    Parameters:
        question (dict): Dictionary containing question data

    Returns:
        None
    """
    logger.debug(f"Displaying question: {question['question']}")
    print(f"\n{question['question']}")
    for i, option in enumerate(question['options'], 1):
        print(f"{i}. {option}")

def get_valid_answer(max_options: int) -> str:
    """
    Get and validate user input.

    Parameters:
        max_options (int): Maximum number of options available

    Returns:
        str: Validated user input
    """
    logger.debug(f"Getting valid answer for {max_options} options")
    while True:
        answer = input(f"\nEnter your answer (1-{max_options}): ")
        if answer.isdigit() and 1 <= int(answer) <= max_options:
            logger.debug(f"Valid answer received: {answer}")
            return answer
        print(f"Invalid input. Please enter a number between 1 and {max_options}.")
        logger.warning(f"Invalid input received: {answer}")

def calculate_percentage(score: int, total_possible: int) -> float:
    """
    Calculate score percentage.

    Parameters:
        score (int): Current score
        total_possible (int): Maximum possible score

    Returns:
        float: Percentage score
    """
    logger.debug(f"Calculating percentage for score {score}/{total_possible}")
    return (score / total_possible) * 100 if total_possible > 0 else 0

def display_final_score(score: int, total_possible: int) -> None:
    """
    Display final score and percentage.

    Parameters:
        score (int): Final score
        total_possible (int): Maximum possible score

    Returns:
        None
    """
    percentage = calculate_percentage(score, total_possible)
    print("\n=== Quiz Complete! ===")
    print(f"Your score: {score}/{total_possible}")
    print(f"Percentage: {percentage:.1f}%")
    
    if percentage == 100:
        print("Perfect score! Excellent job!")
    elif percentage >= 70:
        print("Great job!")
    else:
        print("Keep practicing!")
    
    logger.info(f"Final score displayed: {score}/{total_possible} ({percentage:.1f}%)")

def play_quiz() -> None:
    """
    Main game loop.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting new quiz game")
    display_welcome()
    
    questions = QUIZ_QUESTIONS.copy()
    random.shuffle(questions)
    
    score = 0
    total_possible = sum(q["points"] for q in questions)
    
    logger.debug(f"Total possible score: {total_possible}")

    for question in questions:
        display_question(question)
        user_answer = get_valid_answer(len(question["options"]))
        
        if user_answer == question["correct_answer"]:
            print("Correct!")
            score += question["points"]
            logger.debug(f"Correct answer. Score increased to {score}")
        else:
            correct_option = question["options"][int(question["correct_answer"]) - 1]
            print(f"Sorry, that's incorrect. The correct answer was: {correct_option}")
            logger.debug("Incorrect answer")
        
        time.sleep(1)  # Pause before next question

    display_final_score(score, total_possible)

def main() -> None:
    """
    Main program loop.

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
        
        if play_again == 'no':
            print("\nThanks for playing! Goodbye!")
            logger.info("Game ended by user")
            break

if __name__ == "__main__":
    main()