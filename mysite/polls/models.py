import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class Question(models.Model):
    # 每个字段都是 Field 类的实例 
    # 字符字段被表示为 CharField
    question_text = models.CharField(max_length=200)
    # 日期时间字段被表示为 DateTimeField 
    pub_date = models.DateTimeField('date published')

    # 用于命令行对象调试
    def __str__(self):
        return self.question_text
 
    # 自定义方法
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    # 外键，每个 Choice 对象都关联到一个 Question 对象
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # 整型加默认值
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
