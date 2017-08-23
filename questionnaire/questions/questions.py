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
                                  slug=question['slug'],
                                  hints=question['hints'],
                                  answer=question['answer'],
                                  score=question['score'], 
                                  quiz=Quiz.objects.get(slug=question['quiz-slug']))
            ques.save()

        for mcq in mcqs:
            ques = MCQ.create(question=mcq['question'],
                              slug=mcq['slug'],
                              hints=mcq['hints'], 
                              choices=mcq['choices'], 
                              correct=int(mcq['correct']), 
                              score=mcq['score'], 
                              quiz=Quiz.objects.get(slug=mcq['quiz-slug']))
            ques.save()
    return filename

"""
example: add such object to questions.json
{
  "QUESTIONS": [
    {
      "question": "What is the full form of IP?",
      "slug": "IP-sq",
      "hints": "Seriously?!",
      "answer": "Internet Protocol",
      "score": 10,
      "quiz-slug": "test_quiz"
    }
  ],
  "MCQS": [
    {
      "question": "What is the full form of IP?",
      "slug": "IP-mcq",
      "hints": "Seriously?!",
      "choices": [
        "Internet Programs",
        "Internet Protocol",
        "Internal Protocol",
        "International Protocol"
      ],
      "correct": 2,
      "score": 10,
      "quiz-slug": "test_quiz"
    }
  ]
}
"""
