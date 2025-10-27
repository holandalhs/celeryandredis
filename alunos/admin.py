from django.contrib import admin
from .models import Aluno, Curso, Turma, Matricula

##arquivo: models.py
###Define a estrutura do banco (tabelas, campos, relações)/classes
##arquivo: admin.py
###Diz ao Django como mostrar essas tabelas no painel administrativo/admin
##arquivo: views.py
###Define a lógica de exibição dos dados na interface web (HTML)/funções
##arquivo: urls.py
###Define as rotas/URLs do site e quais views elas chamam
###Para acessar o Django Admin:
###http://127.0.0.1:8000/admin → painel web para gerenciar os dados

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "email", "criado_em")
    search_fields = ("nome", "cpf", "email")
#Diz: “quero que o modelo Aluno apareça no painel, 
# com essas colunas e filtros de busca”.

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nome", "codigo", "ativo") #as colunas
    list_filter = ("ativo",)                  #filtros laterais
    search_fields = ("nome", "codigo")      
#Exibe o modelo Curso com as colunas desejadas.


@admin.register(Turma) # registra o modelo Turma para aparecer no  painel admin
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "curso", "ano", "semestre", "vagas") #as colunas
    list_filter = ("ano", "semestre", "curso") #filtros laterais
    search_fields = ("codigo", "curso__nome", "curso__codigo") #filtros de busca

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "turma", "status", "criado_em")
    list_filter = ("status", "turma__curso", "turma__ano", "turma__semestre")
    search_fields = ("aluno__nome", "aluno__cpf", "turma__codigo", "turma__curso__nome")




















"""
admin.py — é criado automaticamente sempre que você cria um novo app Django (como o alunos) com o comando:

python manage.py startapp alunos


vamos entender por que ele existe e qual a sua função real 👇

🧩 Função do admin.py

O Django já vem com um painel administrativo pronto (o famoso Django Admin).
Esse painel permite:

cadastrar, editar e excluir registros dos modelos (tabelas do banco);

filtrar, buscar, paginar e visualizar dados de forma prática;

controlar permissões de usuários.

O arquivo admin.py serve para registrar os modelos (models.py) dentro desse painel.

⚙️ sem o admin.py

Se você não registrar o modelo no admin.py, ele não aparece no painel do Django Admin
(acessado em http://127.0.0.1:8000/admin).

Ou seja, mesmo que o banco exista e as tabelas estejam criadas, o admin não saberá que elas existem até você registrar.
"""
