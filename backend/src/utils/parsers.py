from typing import List
from langchain_core.output_parsers import StrOutputParser

class QuestionArrayOutputParser(StrOutputParser):
     def parse(self, text: str) -> List[str]:
          # Split the text by newline characters to get individual questions
          questions = text.strip().split("\n")
          # Filter out any empty questions that might occur due to extra new lines
          questions = [q.strip() for q in questions if q.strip()]
          questions_array = [question.strip() for question in questions if question.strip()]
          return questions_array