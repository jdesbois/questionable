from django import template
from main.models import Question

register = template.Library()

@register.inclusion_tag('main/questions.html')

def get_question_list():
return {'questions': Question.objects.all()}