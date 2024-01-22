from django.contrib import admin
from .models import Question, Choice

# Register your models here.
# admin.site.register(Question)
# admin.site.register(Choice)

# Altera a ordem da apresentação dos campos do formulario para edção do Question
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ["pub_date", "question_text"]

# Dividindo formulário em grupos
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ("Texto", {"fields": ["question_text"]}),
#         ("Datas", {"fields": ["pub_date"]}),
#     ]


# Acrescenta em Question, três Choices por padrão além dos existentes (em linha)
# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 1

# Acrescenta em Question, três Choices por padrão além dos existentes (em tabela)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}), # colapse torna o campo minimizado
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"] # apresentando mais dados na apresentação das questions
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)