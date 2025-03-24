"""
quiz_game.py

A multiple-choice quiz game that tracks user score and allows replaying.

Functions:
    display_welcome(): Displays welcome message
    get_valid_input(valid_choices: list) -> str: Gets and validates user input
    present_question(question: dict, question_num: int) -> bool: Presents a question and checks answer
    play_quiz() -> None: Main game function
    display_results(score: int, total: int) -> None: Shows final score
    play_again() -> bool: Asks if user wants to play again

Command Line Usage Example:
    python quiz_game.py
"""

import random
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Quiz questions and answers
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "choices": ["London", "Berlin", "Paris", "Madrid"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest mammal in the world?",
        "choices": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "correct_answer": "Blue Whale"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "choices": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct_answer": "Leonardo da Vinci"
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
    print("Answer the multiple-choice questions by entering the letter of your choice.")
    print("Let's begin!\n")

def get_valid_input(valid_choices: List[str]) -> str:
    """
    Gets and validates user input.

    Parameters:
        valid_choices (List[str]): List of valid input choices

    Returns:
        str: Validated user input
    """
    logger.debug(f"Valid choices: {valid_choices}")
    
    while True:
        user_input = input("Your answer (enter the letter): ").upper()
        if user_input in valid_choices:
            logger.debug(f"Valid input received: {user_input}")
            return user_input
        logger.warning(f"Invalid input received: {user_input}")
        print(f"Invalid input! Please enter one of: {', '.join(valid_choices)}")

def present_question(question: Dict, question_num: int) -> bool:
    """
    Presents a question and checks if the answer is correct.

    Parameters:
        question (Dict): Dictionary containing question data
        question_num (int): Current question number

    Returns:
        bool: True if answer is correct, False otherwise
    """
    logger.debug(f"Presenting question {question_num}")
    
    print(f"\nQuestion {question_num}:")
    print(question["question"])
    
    # Create answer choices mapping
    choices = question["choices"]
    choice_letters = ['A', 'B', 'C', 'D']
    
    # Display choices
    for letter, choice in zip(choice_letters, choices):
        print(f"{letter}. {choice}")
    
    # Get user's answer
    user_answer = get_valid_input(choice_letters)
    selected_answer = choices[choice_letters.index(user_answer)]
    
    is_correct = selected_answer == question["correct_answer"]
    logger.debug(f"Answer correct: {is_correct}")
    
    # Display result
    if is_correct:
        print("Correct! ✓")
    else:
        print(f"Wrong! The correct answer was: {question['correct_answer']} ✗")
    
    return is_correct

def display_results(score: int, total: int) -> None:
    """
    Displays final quiz results.

    Parameters:
        score (int): Number of correct answers
        total (int): Total number of questions

    Returns:
        None
    """
    logger.debug(f"Displaying results - Score: {score}/{total}")
    
    percentage = (score / total) * 100
    print("\n=== Quiz Complete! ===")
    print(f"Your score: {score} out of {total}")
    print(f"Percentage: {percentage:.1f}%")
    
    # Display performance message
    if percentage == 100:
        print("Perfect score! Excellent! 🏆")
    elif percentage >= 80:
        print("Great job! 🌟")
    elif percentage >= 60:
        print("Good effort! 👍")
    else:
        print("Keep practicing! 📚")

def play_again() -> bool:
    """
    Asks if the user wants to play another round.

    Parameters:
        None

    Returns:
        bool: True if user wants to play again, False otherwise
    """
    logger.debug("Asking to play again")
    
    while True:
        choice = input("\nWould you like to play again? (y/n): ").lower()
        if choice in ['y', 'n']:
            logger.debug(f"Play again choice: {choice}")
            return choice == 'y'
        print("Please enter 'y' for yes or 'n' for no.")

def play_quiz() -> None:
    """
    Main game function that runs the quiz.

    Parameters:
        None

    Returns:
        None
    """
    logger.info("Starting new quiz game")
    
    display_welcome()
    
    while True:
        # Shuffle questions for variety
        questions = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS))
        score = 0
        
        # Present each question
        for i, question in enumerate(questions, 1):
            if present_question(question, i):
                score += 1
        
        # Display final results
        display_results(score, len(questions))
        
        # Ask to play again
        if not play_again():
            print("\nThanks for playing! Goodbye! 👋")
            break

if __name__ == "__main__":
    try:
        play_quiz()
    except KeyboardInterrupt:
        logger.info("Game interrupted by user")
        print("\n\nGame interrupted. Goodbye! 👋")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print("\nAn unexpected error occurred. Please try again.")