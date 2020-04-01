from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question
from django.http import Http404
from django.urls import reverse


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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST 可通过关键字名获取提交数据，此处以字符串享实返回选择的 Choice id
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 如果 choice 不存在则引发 keyerror，跳转到问题 detail 页面并告知错误
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # 投票后，投票值加1
        selected_choice.votes += 1
        selected_choice.save()
        # 投票完成后将用户重定向到结果，防止用户点击两次按钮
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
