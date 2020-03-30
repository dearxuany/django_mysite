from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question
from django.http import Http404


# Create your views here
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 格式写死的前五个
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)

    # 使用 template
    template = loader.get_template('polls/index.html')
    context = {
        # 传递字典，填充上下文
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    # 如果问题细节不存在，则返回404
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, 'polls/detail.html',{'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
