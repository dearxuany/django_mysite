from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.http import Http404
from django.urls import reverse
from django.views import generic

# ListView 显示一个对象列表
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# DetailView 显示一个特定类型对象详细信息
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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
