import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Crie uma pergunta com o "question_text" fornecido e publique o
    dado com número de 'dias' deslocados para agora (
      negativo para as questões publicadas no passado,
      positivo para as questões ainda não publicadas
    ).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Se não houver dúvidas, uma mensagem apropriada será exibida.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não há enquetes disponíveis.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Perguntas com um pub_date no passado são exibidas no página de índice.
        """
        question = create_question(question_text="Questão antiga - 1.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Perguntas com um pub_date no futuro não são exibidas em
        a página de índice.
        """
        create_question(question_text="Questão Futura.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "Não há enquetes disponíveis.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Mesmo que existam questões passadas e futuras, apenas questões passadas
        são exibidos.
        """
        question = create_question(question_text="Questão antiga -.", days=-30)
        create_question(question_text="Questão Futura.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        A página de índice de perguntas pode exibir várias perguntas.
        """
        question1 = create_question(question_text="Questão antiga - 1.", days=-30)
        question2 = create_question(question_text="Questão antiga - 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )