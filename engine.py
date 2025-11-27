from typing import List, Tuple, Optional

from model import PhysicsModel


class ChatEngine:
    def __init__(self):
        self.model = PhysicsModel()

    def handle(
        self,
        message: str,
        class_level: Optional[int] = None,
        topic: Optional[str] = None,
    ) -> Tuple[str, List[str]]:
        """
        Returns (answer_text, related_questions)
        """
        text = (message or "").strip()
        if not text:
            return "Please type a question about Physics.", []

        low = text.lower()

        if low in {"hi", "hello", "hey"}:
            return "Hello! Ask me any Physics question from classes 8–12.", []

        if "help" in low or "what can you do" in low:
            return (
                "I am an offline Physics assistant for NCERT classes 8–12.\n"
                "You can ask conceptual questions like:\n"
                "- What is Newton's first law?\n"
                "- Define kinetic energy.\n"
                "- Difference between speed and velocity.\n"
                "Optionally choose class and topic to get more focused answers."
            ), []

        if low in {"bye", "exit", "quit"}:
            return "Goodbye! Keep learning Physics.", []

        best, related = self.model.query(
            text,
            class_level=class_level,
            topic=topic,
            top_k=3,
            min_sim=0.2,
        )

        if not best:
            return (
                "I am not confident about that question yet.\n"
                "Please rephrase it, or try a different Physics topic I know.",
                [],
            )

        sim, entry = best
        ans = entry.get("answer", "").strip()
        topic_name = entry.get("topic", "Physics")
        lvl = entry.get("class_level", None)

        header = f"[Class {lvl}] {topic_name}" if lvl else topic_name
        main = f"{header}\n\n{ans}"

        related_questions: List[str] = []
        for _, e in related:
            q = e.get("question", "").strip()
            if q:
                related_questions.append(q)

        return main, related_questions