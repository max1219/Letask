from dataclasses import dataclass
from services.question import Question


@dataclass
class UserRecord:
    user_id: int
    questions: list[Question]
