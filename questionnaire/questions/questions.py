import json

from questionnaire.models import SimpleQuestion, MCQ, Quiz

JSON_FILEPATH = 'questionnaire/questions/'
JSON_FILENAME = 'questions.json'


def addquestions(filename=JSON_FILEPATH + JSON_FILENAME):
    with open(filename) as jsonfile:
        quesjson = json.load(jsonfile)
        questions = quesjson['QUESTIONS']
        mcqs = quesjson['MCQS']

        for question in questions:
            ques = SimpleQuestion(question=question['question'],
                                  hints=question['hints'],
                                  answer=question['answer'],
                                  score=question['score'], 
                                  quiz=Quiz.objects.get(pk=question['quiz']))
            ques.save()

        for mcq in mcqs:
            ques = MCQ.create(question=mcq['question'], 
                              hints=mcq['hints'], 
                              choices=mcq['choices'], 
                              correct=int(mcq['correct']), 
                              score=mcq['score'], 
                              quiz=Quiz.objects.get(pk=mcq['quiz']))
            ques.save()
    return filename

"""
example: add such object to question.json
{
  "QUESTIONS": [
    {
      "question": "What is the full form of IP?",
      "hints": "Seriously?!",
      "answer": "Internet Protocol",
      "score": 10,
      "quiz": 1
    }
  ],
  "MCQS": [
    {
      "question": "What is the full form of IP?",
      "hints": "Seriously?!",
      "choices": [
        "Internet Programs",
        "Internet Protocol",
        "Internal Protocol",
        "International Protocol"
      ],
      "correct": 2,
      "score": 10,
      "quiz": 1
    }
  ]
}
"""
