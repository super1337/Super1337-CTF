from django.shortcuts import render
from .models import Question, MultipleChoiceQuestion

def mcq(request):
    que=MultipleChoiceQuestion.objects.all()
    questions=[]
    p=0
    for h in que:
        p+=1
        q=0
        qu = [h['question']]
        ch=[]
        for i in h.choices:
            q+=1
            ch+=[[q,i]]
        qu+=[[ch]]
        questions+=[qu]

    return render(request,'questionnaire/mcq.html',{'questions':questions})
