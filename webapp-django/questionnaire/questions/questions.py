import json

from questionnaire.models import Question, MultipleChoiceQuestion

JSON_FILEPATH = 'questionnaire/questions/'
JSON_FILENAME = 'questions.json'


def addquestions(filename=JSON_FILEPATH+JSON_FILENAME):
    with open(filename) as jsonfile:
        quesjson = json.load(jsonfile)
        questions = quesjson['QUESTIONS']
        mcqs = quesjson['MCQS']

        for question in questions:
            ques = Question(question=question['question'],
                            hints=question['hints'],
                            answer=question['answer'])
            ques.save()

        for mcq in mcqs:
            ques = MultipleChoiceQuestion.create(question=mcq['question'],
                                                 hints=mcq['hints'],
                                                 choices=mcq['choices'],
                                                 correct=int(mcq['correct']))
            ques.save()
    return filename
