# app/services/scoring_service.py
from typing import Iterable, Dict, Tuple

from app.models.question import Question, DifficultyEnum

DIFFICULTY_POINTS = {
    DifficultyEnum.easy: 1,
    DifficultyEnum.medium: 2,
    DifficultyEnum.hard: 3,
}


def calculate_score(
    questions: Iterable[Question],
    answers: Dict[int, str],
) -> Tuple[int, int, int, int]:
    """
    Calcula el puntaje total, puntaje máximo posible,
    número de respuestas correctas e incorrectas.

    :param questions: lista de preguntas de la trivia
    :param answers: diccionario {question_id: opción_elegida}
    """
    total_score = 0
    max_score = 0
    correct = 0
    wrong = 0

    for q in questions:
        points = DIFFICULTY_POINTS[q.difficulty]
        max_score += points

        user_answer = answers.get(q.id)
        if user_answer is not None and user_answer == q.correct_option:
            total_score += points
            correct += 1
        else:
            # si respondió mal o no respondió, la contamos como incorrecta
            wrong += 1

    return total_score, max_score, correct, wrong
