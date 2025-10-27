from django.urls import path
from . import views

app_name = "alunos"

urlpatterns = [
    path("matriculas/", views.matriculas_list, name="matriculas_list"),
]
