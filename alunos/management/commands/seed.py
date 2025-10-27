from django.core.management.base import BaseCommand
from alunos.models import Curso, Turma, Aluno, Matricula
##Os dois arquivos __init__.py precisam existir, mesmo vazios,
##pois eles fazem o Django reconhecer a pasta como um pacote de comandos.

class Command(BaseCommand):
    help = "Popula o banco de dados com dados de exemplo para testes."

    def handle(self, *args, **options):
        # Cursos
        tsi, _ = Curso.objects.get_or_create(
            nome="Tecnologia em Sistemas para Internet",
            codigo="TSI",
        )
        ctb, _ = Curso.objects.get_or_create(
            nome="Contabilidade",
            codigo="CTB",
        )

        # Turmas
        t1, _ = Turma.objects.get_or_create(
            curso=tsi,
            codigo="TSI-2025.1-A",
            defaults={"ano": 2025, "semestre": 1, "vagas": 40},
        )
        t2, _ = Turma.objects.get_or_create(
            curso=ctb,
            codigo="CTB-2025.1-A",
            defaults={"ano": 2025, "semestre": 1, "vagas": 50},
        )

        # Alunos
        a1, _ = Aluno.objects.get_or_create(
            nome="Luanna Siqueira",
            cpf="000.000.000-00",
            defaults={"email": "luanna@example.com"},
        )
        a2, _ = Aluno.objects.get_or_create(
            nome="João Silva",
            cpf="111.111.111-11",
            defaults={"email": "joao@example.com"},
        )

        # Matrículas
        Matricula.objects.get_or_create(
            aluno=a1,
            turma=t1,
            defaults={"status": Matricula.Status.CONFIRMADA},
        )
        Matricula.objects.get_or_create(
            aluno=a2,
            turma=t1,
            defaults={"status": Matricula.Status.PENDENTE},
        )
        Matricula.objects.get_or_create(
            aluno=a2,
            turma=t2,
            defaults={"status": Matricula.Status.CANCELADA},
        )

        self.stdout.write(self.style.SUCCESS("✅ Dados de exemplo criados com sucesso!"))
