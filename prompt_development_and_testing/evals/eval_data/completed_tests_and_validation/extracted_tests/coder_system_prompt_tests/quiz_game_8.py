"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows replaying.

Functions:
    display_welcome(): Displays welcome message
    get_valid_choice(max_choice: int) -> str: Gets and validates user input
    run_quiz(questions: list) -> tuple: Runs the quiz and returns score
    play_again() -> bool: Asks if user wants to play again
    main(): Main game loop

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

# Quiz questions and answers
QUIZ_DATA = [
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
        "question": "What is 2 + 2?",
        "choices": ["3", "4", "5", "6"],
        "correct": "2"  # 4
    },
    {
        "question": "Who painted the Mona Lisa?",
        "choices": ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
        "correct": "2"  # Da Vinci
    },
    {
        "question": "What is the largest mammal in the world?",
        "choices": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        "correct": "2"  # Blue Whale
    }
]

def display_welcome() -> None:
    """
    Displays welcome message and game instructions.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Displaying welcome message")
    print("\n=== Welcome to the Quiz Game! ===")
    print("Answer the multiple-choice questions by entering the number of your choice.")
    print("Let's begin!\n")

def get_valid_choice(max_choice: int) -> str:
    """
    Gets and validates user input for quiz choices.

    Parameters:
        max_choice (int): Maximum number of choices available

    Returns:
        str: Validated user choice
    """
    while True:
        choice = input(f"Enter your choice (1-{max_choice}): ")
        logger.debug(f"User input: {choice}")
        
        if choice.isdigit() and 1 <= int(choice) <= max_choice:
            return choice
        
        logger.warning(f"Invalid input: {choice}")
        print(f"Please enter a number between 1 and {max_choice}")

def run_quiz(questions: List[Dict]) -> Tuple[int, int]:
    """
    Runs the quiz game.

    Parameters:
        questions (List[Dict]): List of question dictionaries

    Returns:
        Tuple[int, int]: Tuple containing (score, total_questions)
    """
    logger.info("Starting quiz")
    score = 0
    total_questions = len(questions)
    
    # Shuffle questions for variety
    random.shuffle(questions)
    
    for i, question_data in enumerate(questions, 1):
        print(f"\nQuestion {i} of {total_questions}:")
        print(question_data["question"])
        
        # Display choices
        for idx, choice in enumerate(question_data["choices"], 1):
            print(f"{idx}. {choice}")
        
        # Get user's answer
        user_answer = get_valid_choice(len(question_data["choices"]))
        
        # Check if correct
        if user_answer == question_data["correct"]:
            print("Correct!")
            score += 1
            logger.debug(f"Correct answer - Current score: {score}")
        else:
            correct_choice = question_data["choices"][int(question_data["correct"]) - 1]
            print(f"Sorry, that's incorrect. The correct answer was: {correct_choice}")
            logger.debug(f"Incorrect answer - Current score: {score}")
    
    logger.info(f"Quiz completed. Final score: {score}/{total_questions}")
    return score, total_questions

def play_again() -> bool:
    """
    Asks if the user wants to play another round.

    Parameters:
        None

    Returns:
        bool: True if user wants to play again, False otherwise
    """
    while True:
        choice = input("\nWould you like to play again? (yes/no): ").lower()
        logger.debug(f"Play again choice: {choice}")
        
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def main() -> None:
    """
    Main game loop.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting game")
    display_welcome()
    
    while True:
        score, total = run_quiz(QUIZ_DATA)
        percentage = (score / total) * 100
        
        print("\n=== Game Over ===")
        print(f"Your final score: {score}/{total} ({percentage:.1f}%)")
        
        if percentage == 100:
            print("Perfect score! Congratulations!")
        elif percentage >= 70:
            print("Great job!")
        elif percentage >= 50:
            print("Good effort!")
        else:
            print("Keep practicing!")
        
        if not play_again():
            print("\nThanks for playing! Goodbye!")
            logger.info("Game ended")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        logger.warning("Game interrupted by user")
    except Exception as e:
        print("\nAn error occurred. The game has to close.")
        logger.error(f"Unexpected error: {e}")