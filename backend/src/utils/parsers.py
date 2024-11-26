from langchain_core.output_parsers import StrOutputParser

class QuestionArrayOutputParser(StrOutputParser):
     def parse(self, text: str):
          # Split the text by newline characters to get individual questions
          questions = text.strip().split("\n\n")
          # Filter out any empty questions that might occur due to extra new lines
          questions = [q.strip() for q in questions if q.strip()]
          return questions