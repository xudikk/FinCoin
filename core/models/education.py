from django.db import models

from core.models import User, Algorithm


class Student(models.Model):
    student = models.ForeignKey(User, limit_choices_to={"ut": 3}, on_delete=models.CASCADE)
    algratim = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    type = models.CharField(max_length=128, choices=[
        ("Bajarilmoqda", "Bajarilmoqda"),
        ("Bajarildi", "Bajarildi")
    ])

    def __str__(self):
        return f"{self.student.first_name}"

    class Meta:
        verbose_name_plural = "S. Student Algorithm"


class Teacher(models.Model):
    teacher = models.ForeignKey(User, limit_choices_to={"ut": 2}, on_delete=models.CASCADE)
    oquvchi = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ustoz: {self.teacher} | O'quvchi: {self.oquvchi}"

    class Meta:
        verbose_name_plural = "U. Ustozlar"
