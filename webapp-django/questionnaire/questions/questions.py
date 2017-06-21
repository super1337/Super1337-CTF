import json

from questionnaire.models import SimpleQuestion, MultipleChoiceQuestion

JSON_FILEPATH = 'questionnaire/questions/'
JSON_FILENAME = 'questions.json'


def addquestions(filename=JSON_FILEPATH+JSON_FILENAME):
    with open(filename) as jsonfile:
        quesjson = json.load(jsonfile)
        questions = quesjson['QUESTIONS']
        mcqs = quesjson['MCQS']

        for question in questions:
            ques = SimpleQuestion(question=question['question'],
                                  hints=question['hints'],
                                  answer=question['answer'],
                                  score=question['score'])
            ques.save()

        for mcq in mcqs:
            ques = MultipleChoiceQuestion.create(question=mcq['question'],
                                                 hints=mcq['hints'],
                                                 choices=mcq['choices'],
                                                 correct=int(mcq['correct'],
                                                             score=question['score']))
            ques.save()
    return filename
