"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows for replay.

Functions:
    display_welcome(): Displays welcome message
    get_valid_choice(max_choice: int) -> str: Gets and validates user input
    run_quiz(questions: list) -> tuple: Runs a single quiz session
    play_game() -> None: Main game loop
    display_results(score: int, total: int) -> None: Shows quiz results

Command Line Usage Example:
    python quiz_game.py
"""

import random
import logging
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Quiz questions stored as a list of dictionaries
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "choices": ["London", "Berlin", "Paris", "Madrid"],
        "correct": "3"  # Paris
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": "2"  # Mars
    },
    {
        "question": "What is the largest mammal in the world?",
        "choices": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct": "2"  # Blue Whale
    },
    {
        "question": "Who painted the Mona Lisa?",
        "choices": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
        "correct": "2"  # Da Vinci
    },
    {
        "question": "What is the chemical symbol for gold?",
        "choices": ["Ag", "Fe", "Au", "Cu"],
        "correct": "3"  # Au
    }
]

def display_welcome() -> None:
    """
    Displays the welcome message for the quiz game.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Displaying welcome message")
    print("\n=== Welcome to the Quiz Game! ===")
    print("Answer the following multiple-choice questions.")
    print("Choose the number corresponding to your answer.")

def get_valid_choice(max_choice: int) -> str:
    """
    Gets and validates user input for quiz choices.

    Parameters:
        max_choice (int): Maximum number of choices available

    Returns:
        str: Validated user choice
    """
    while True:
        choice = input("Your answer (enter the number): ").strip()
        logger.debug(f"User input: {choice}")
        
        if not choice.isdigit():
            logger.warning("Invalid input: not a number")
            print("Please enter a number.")
            continue
            
        if not (1 <= int(choice) <= max_choice):
            logger.warning(f"Invalid input: outside range 1-{max_choice}")
            print(f"Please enter a number between 1 and {max_choice}.")
            continue
            
        return choice

def run_quiz(questions: List[Dict]) -> Tuple[int, int]:
    """
    Runs a single quiz session.

    Parameters:
        questions (List[Dict]): List of question dictionaries

    Returns:
        Tuple[int, int]: Score and total number of questions
    """
    score = 0
    total = len(questions)
    
    logger.info(f"Starting quiz with {total} questions")
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question['question']}")
        for j, choice in enumerate(question['choices'], 1):
            print(f"{j}. {choice}")
            
        user_answer = get_valid_choice(len(question['choices']))
        
        if user_answer == question['correct']:
            print("Correct!")
            score += 1
            logger.debug(f"Correct answer - Current score: {score}")
        else:
            correct_answer = question['choices'][int(question['correct'])-1]
            print(f"Sorry, that's incorrect. The correct answer was: {correct_answer}")
            logger.debug(f"Incorrect answer - Score remains: {score}")
    
    logger.info(f"Quiz completed. Final score: {score}/{total}")
    return score, total

def display_results(score: int, total: int) -> None:
    """
    Displays the quiz results.

    Parameters:
        score (int): Number of correct answers
        total (int): Total number of questions

    Returns:
        None
    """
    logger.debug(f"Displaying results - Score: {score}/{total}")
    percentage = (score / total) * 100
    print("\n=== Quiz Results ===")
    print(f"You got {score} out of {total} questions correct!")
    print(f"Your score: {percentage:.1f}%")
    
    if percentage == 100:
        print("Perfect score! Excellent job!")
    elif percentage >= 80:
        print("Great job!")
    elif percentage >= 60:
        print("Good effort!")
    else:
        print("Keep practicing!")

def play_game() -> None:
    """
    Main game loop that handles the quiz flow.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        display_welcome()
        questions = QUIZ_QUESTIONS.copy()
        random.shuffle(questions)
        
        score, total = run_quiz(questions)
        display_results(score, total)
        
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").lower().strip()
            logger.debug(f"Play again response: {play_again}")
            
            if play_again in ['yes', 'no']:
                break
            print("Please enter 'yes' or 'no'.")
        
        if play_again == 'no':
            print("\nThanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    play_game()