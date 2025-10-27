from celery import shared_task              # indica que é uma tarefa compartilhada entre apps do projeto
#O VSC não vai aplicar checagem de tipo dentro do celery, e ele tenta analisar estaticamente os tipos
#das funções e classes da lib celery (por exemplo, shared_task, Celery, etc.)
from django.utils import timezone           # para lidar com datas e horas (aware)
from django.conf import settings            # para acessar configurações do projeto
from datetime import timedelta, datetime    # timedelta = intervalo de tempo; datetime = data/hora padrão
from pathlib import Path                    # para manipular caminhos de arquivos
import csv                                  # para ler e escrever arquivos CSV
from typing import Optional               # para tipos opcionais 

from .models import Matricula # importa o modelo Matricula

@shared_task
def gerar_relatorio_matriculas():
    """Gera um CSV com totalizações simples por status."""
    base = Path(settings.MEDIA_ROOT) / "reports" # pasta para salvar relatórios
    base.mkdir(parents=True, exist_ok=True) # cria a pasta se não existir

    now = timezone.localtime() # data e hora local
    filename = base / f"matriculas_{now:%Y%m%d_%H%M%S}.csv" # nome do arquivo com timestamp

    qs = Matricula.objects.select_related("turma__curso") # consulta otimizada
    total = qs.count() # total de matrículas
    por_status = {}
    for st, _ in Matricula.Status.choices:
        por_status[st] = qs.filter(status=st).count() # total por status

    # Gera o arquivo CSV
    with filename.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";") # cria o escritor CSV
        w.writerow(["Relatório de Matrículas", f"Gerado em {now:%d/%m/%Y %H:%M}"]) # cabeçalho
        w.writerow([]) # linha em branco
        w.writerow(["Total de Matrículas", total]) # total geral
        for st, qt in por_status.items():
            w.writerow([st, qt]) # total por status
    
    # Opcional: também listar cada matrícula
    with filename.open("a", newline="", encoding="utf-8") as f:
         w = csv.writer(f, delimiter=";")
         w.writerow([])
         w.writerow(["Aluno", "CPF", "Curso", "Turma", "Ano/Sem", "Status", "Criado em"])
         for m in qs:
             w.writerow([
                 m.aluno.nome, m.aluno.cpf, m.turma.curso.codigo, m.turma.codigo,
                 f"{m.turma.ano}/{m.turma.semestre}", m.get_status_display(),
                 timezone.localtime(m.criado_em).strftime("%d/%m/%Y %H:%M")
             ])

    return str(filename) # retorna o caminho do arquivo gerado


@shared_task                    #pode ser int ou None
def limpar_relatorios_antigos(days: Optional[int] = None) -> dict:
    """
    Remove CSVs em MEDIA_ROOT/reports mais antigos que N dias.
    Se 'days' for None, usa settings.REPORTS_RETENTION_DAYS (padrão 7).
    """
    # garanta que é int
    keep_days: int = int(days) if days is not None else int(getattr(settings, "REPORTS_RETENTION_DAYS", 7))

    base = Path(settings.MEDIA_ROOT) / "reports"
    base.mkdir(parents=True, exist_ok=True)

    limite = timezone.now() - timedelta(days=keep_days)

    removidos: list[str] = []
    mantidos: list[str] = []

    tz = timezone.get_current_timezone()

    for p in base.glob("*.csv"):
        try:
            # mtime (timestamp float) -> datetime naive -> datetime aware no timezone atual
            mtime_naive = datetime.fromtimestamp(p.stat().st_mtime)
            mtime = timezone.make_aware(mtime_naive, tz)
        except Exception:
            mantidos.append(p.name)
            continue

        if mtime < limite:
            try:
                p.unlink()
                removidos.append(p.name)
            except Exception:
                mantidos.append(p.name)
        else:
            mantidos.append(p.name)

    return {
        "retention_days": keep_days,
        "removed_count": len(removidos),
        "kept_count": len(mantidos),
        "removed": removidos,
    }