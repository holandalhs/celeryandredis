from django.shortcuts import render # Importa render para renderizar templates
from django.core.paginator import Paginator # Importa Paginator para paginação
from django.db.models import Q # Importa Q para consultas complexas
from .models import Matricula # Importa o modelo Matricula

def matriculas_list(request):
    q = request.GET.get("q", "").strip()  # Obtém o termo de busca da query string
    status = request.GET.get("status", "") # Obtém o filtro de status da query string
    curso = request.GET.get("curso", "")  # Obtém o filtro de curso da query string
    ano = request.GET.get("ano", "")      # Obtém o filtro de ano da query string
    semestre = request.GET.get("semestre", "") # Obtém o filtro de semestre da query string

    qs = Matricula.objects.select_related("aluno", "turma", "turma__curso") 
    # Otimiza consultas relacionadas

    if q: # Se houver termo de busca
        qs = qs.filter(
            Q(aluno__nome__icontains=q) | # busca por nome do aluno
            Q(aluno__cpf__icontains=q) | # busca por CPF do aluno
            Q(turma__codigo__icontains=q) | # busca por código da turma
            Q(turma__curso__nome__icontains=q) # busca por nome do curso
        )   
    if status: # Se houver filtro de status
        qs = qs.filter(status=status) # Filtra por status
    if curso: # Se houver filtro de curso
        qs = qs.filter(turma__curso__codigo__iexact=curso) # Filtra por curso
    if ano: # Se houver filtro de ano
        qs = qs.filter(turma__ano=ano) # Filtra por ano
    if semestre: # Se houver filtro de semestre
        qs = qs.filter(turma__semestre=semestre) # Filtra por semestre

    paginator = Paginator(qs, 20) # Pagina os resultados, 20 por página
    page_number = request.GET.get("page") # Obtém o número da página da query string
    page_obj = paginator.get_page(page_number) # Obtém o objeto da página

    # para montar selects no template
    cursos = qs.values_list("turma__curso__codigo", flat=True).distinct().order_by("turma__curso__codigo")
    ## cursos distintos na qs, ordenados por código do curso    
    anos = qs.values_list("turma__ano", flat=True).distinct().order_by("-turma__ano")
    ## anos distintos na qs, ordenados do maior para o menor
    semestres = qs.values_list("turma__semestre", flat=True).distinct().order_by("turma__semestre")
    ## semestres distintos na qs, ordenados do menor para o maior

    context = { # contexto para o template
        "page_obj": page_obj, # objeto da página
        "q": q, # termo de busca
        "status_sel": status, # status selecionado
        "curso_sel": curso, # curso selecionado
        "ano_sel": ano,
        "semestre_sel": semestre,
        "cursos": cursos, # lista de cursos para o select
        "anos": anos, # lista de anos para o select
        "semestres": semestres, # lista de semestres para o select
    }

    return render(request, "alunos/matriculas_list.html", context) 
    # Renderiza o template com o contexto
