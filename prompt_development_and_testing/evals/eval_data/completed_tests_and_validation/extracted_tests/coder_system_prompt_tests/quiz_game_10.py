"""
quiz_game.py

A multiple-choice quiz game that tracks user scores and allows for replay.

Classes:
    Question: Stores question data
    Quiz: Manages quiz game logic

Functions:
    play_game(): Runs the main game loop
    get_valid_input(prompt: str, valid_range: range): Gets and validates user input

Command Line Usage Example:
    python quiz_game.py
"""

import random
import time
import logging
from typing import List, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Question:
    """
    Stores question data including the question text, options, and correct answer.
    
    Attributes:
        text (str): The question text
        options (List[str]): List of possible answers
        correct_answer (int): Index of the correct answer in options
    """
    text: str
    options: List[str]
    correct_answer: int

class Quiz:
    """
    Manages the quiz game logic including score tracking and question presentation.
    """
    
    def __init__(self):
        """
        Initializes the quiz with questions and sets initial score.
        
        Parameters:
            None
            
        Returns:
            None
        """
        self.questions = [
            Question(
                "What is the capital of France?",
                ["London", "Berlin", "Paris", "Madrid"],
                2
            ),
            Question(
                "Which planet is known as the Red Planet?",
                ["Venus", "Mars", "Jupiter", "Saturn"],
                1
            ),
            Question(
                "What is the largest mammal in the world?",
                ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
                1
            ),
            Question(
                "Who painted the Mona Lisa?",
                ["Van Gogh", "Da Vinci", "Picasso", "Rembrandt"],
                1
            ),
            Question(
                "What is the chemical symbol for gold?",
                ["Ag", "Fe", "Au", "Cu"],
                2
            )
        ]
        self.score = 0
        self.total_questions = len(self.questions)
        logger.debug(f"Quiz initialized with {self.total_questions} questions")

    def present_question(self, question: Question) -> None:
        """
        Displays a question and its options to the user.
        
        Parameters:
            question (Question): The question to present
            
        Returns:
            None
        """
        logger.debug(f"Presenting question: {question.text}")
        print("\n" + question.text)
        for i, option in enumerate(question.options, 1):
            print(f"{i}. {option}")

    def check_answer(self, question: Question, user_answer: int) -> bool:
        """
        Checks if the user's answer is correct.
        
        Parameters:
            question (Question): The current question
            user_answer (int): The user's answer (1-based index)
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        logger.debug(f"Checking answer: user_answer={user_answer}, correct_answer={question.correct_answer + 1}")
        return user_answer - 1 == question.correct_answer

def get_valid_input(prompt: str, valid_range: range) -> int:
    """
    Gets and validates user input within a specified range.
    
    Parameters:
        prompt (str): The input prompt to display
        valid_range (range): The range of valid inputs
        
    Returns:
        int: The validated user input
    """
    while True:
        try:
            user_input = int(input(prompt))
            if user_input in valid_range:
                logger.debug(f"Valid input received: {user_input}")
                return user_input
            else:
                print(f"Please enter a number between {valid_range.start} and {valid_range.stop - 1}")
        except ValueError:
            print("Please enter a valid number")
            logger.warning("Invalid input received")

def play_game() -> None:
    """
    Runs the main game loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    logger.info("Starting new game")
    quiz = Quiz()
    questions = quiz.questions.copy()
    random.shuffle(questions)

    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i} of {quiz.total_questions}")
        quiz.present_question(question)
        
        answer = get_valid_input("Enter your answer (1-4): ", range(1, 5))
        
        if quiz.check_answer(question, answer):
            print("Correct!")
            quiz.score += 1
        else:
            correct_option = question.options[question.correct_answer]
            print(f"Sorry, that's incorrect. The correct answer was: {correct_option}")
        
        time.sleep(1)  # Pause briefly before next question

    # Display final score
    percentage = (quiz.score / quiz.total_questions) * 100
    print(f"\nGame Over! Your final score: {quiz.score}/{quiz.total_questions} ({percentage:.1f}%)")
    logger.info(f"Game completed. Final score: {quiz.score}/{quiz.total_questions}")

def main():
    """
    Main program loop that allows for multiple games.
    
    Parameters:
        None
        
    Returns:
        None
    """
    while True:
        play_game()
        
        while True:
            play_again = input("\nWould you like to play again? (yes/no): ").lower()
            if play_again in ['yes', 'no']:
                break
            print("Please enter 'yes' or 'no'")
        
        if play_again == 'no':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()