from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Choice, Question

# Create your views here.

# INDEX SEM TEMPLATE: MODELO 1
# def index(request):
#     return HttpResponse(
#         '''
#         <h1>Questionário de Enquete</h1>
#         <h3>Site desenvolvido em django para estudar a criação de sites e apps com o gerenciamento de páginas, usuários, adminstradores, publicações e mais</h3>
#         <b>Dev: Tiago Feitoza</b>
#         '''
#     )
# INDEX SEM TEMPLATE: MODELO 2
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     output = "<br> ".join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# INDEX COM TEMPLATE:
# from django.template import loader
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# INDEX COM TEMPLATE POR RENDER:
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

### OUTRAS VIEWS ###

# Detalhes da Questão: MODELO 1
# def detail(request, question_id):
#     return HttpResponse("Questão: %s" % question_id)

# Detalhes da Questão: MODELO 2 - teste de excessão, sem "detail.html"
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})

# Detalhes da Questão: MODELO 2 - teste de atalho para excessão, sem "detail.html"
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# Modelo Inicial
# def results(request, question_id):
#     response = "Resultado da Questão: %s"
#     return HttpResponse(response % question_id)
# def vote(request, question_id):
#     return HttpResponse("Votando a Questão: %s" % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Você não selecionou uma opção.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))