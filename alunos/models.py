from django.db import models
from django.core.validators import MinValueValidator

##O VS Code (Pylance) tenta aplicar checagem de tipos estática.
##Os campos do Django (models.CharField, etc.) são descritores, e o Pylance não entende isso.
##Ao colocar # type: ignore, você instrui o analisador a ignorar a checagem de tipo dessa linha.


class Aluno(models.Model):
    nome = models.CharField(max_length=120)  # type: ignore
    cpf = models.CharField(max_length=14, unique=True)  # type: ignore
    email = models.EmailField(unique=True)  # type: ignore
    data_nascimento = models.DateField(null=True, blank=True)  # type: ignore
    criado_em = models.DateTimeField(auto_now_add=True)  # type: ignore

    class Meta: # metadados da classe       
        ordering = ["nome"]

    def __str__(self): # representação string do objeto 
        return f"{self.nome} ({self.cpf})"


class Curso(models.Model):
    nome = models.CharField(max_length=120)  # type: ignore
    codigo = models.CharField(max_length=20, unique=True)  # type: ignore
    ativo = models.BooleanField(default=True)  # type: ignore

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} - {self.codigo}"

     

class Turma(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="turmas")  # type: ignore
    codigo = models.CharField(max_length=20)  # type: ignore  # ex: TSI-2025.1-A
    ano = models.PositiveIntegerField()  # type: ignore
    semestre = models.PositiveSmallIntegerField(choices=[(1, "1"), (2, "2")], default=1)  # type: ignore
    vagas = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # type: ignore

    class Meta:
        unique_together = ("curso", "codigo")
        ordering = ["-ano", "-semestre", "curso__nome", "codigo"]

    def __str__(self):
        return f"{self.codigo} ({self.curso.codigo})"


class Matricula(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente" # valor default
        CONFIRMADA = "CONFIRMADA", "Confirmada" # valor confirmado
        CANCELADA = "CANCELADA", "Cancelada"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="matriculas")  # type: ignore
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="matriculas")  # type: ignore
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)  # type: ignore
    criado_em = models.DateTimeField(auto_now_add=True)  # type: ignore

    class Meta:                      #evita matrícula duplicada na mesma turma
        unique_together = ("aluno", "turma") # um aluno não pode se matricular mais de uma vez na mesma turma
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.aluno.nome} -> {self.turma.codigo} [{self.status}]"
        # representação string do objeto

