from django.db import models

from core.models import User


class Course(models.Model):
    name = models.CharField("Kurs Turi", max_length=50, null=False, blank=False)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="course_mentor",
                               limit_choices_to={'ut': 2}
                               )

    def __str__(self):
        return f"{self.name} | Mentor: {self.mentor}"

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "Courses"


class Group(models.Model):
    name = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="course")
    duration = models.CharField("Kurs Davomiyligi", max_length=128, default="6 oy")
    status = models.SmallIntegerField(default=0, choices=[
        (1, "Boshlanmoqda"),
        (2, "Davom Qilyabdi"),
        (3, "Guruh Yopilgan"),
    ])

    def __str__(self):
        return f"Name : {self.name} | Course: {self.course} "


class GroupStudent(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                limit_choices_to={"ut": 3})
    start_date = models.DateField(verbose_name="O'quvchi guruhga qo'shilgan sana", blank=False, null=False)
    end_date = models.DateField(verbose_name="O'quvchi guruhdan chiqqan sana", blank=True, null=True)

    class Meta:
        unique_together = (('student', 'group'),)
        verbose_name = "Guruh Talabasi"
        verbose_name_plural = "Talabalar"

    def __str__(self):
        return f"{self.student}"


class Interested(models.Model):
    name = models.CharField(verbose_name="Ism Familiya", max_length=128, null=False, blank=False)
    phone = models.CharField("Telefon raqam", max_length=20, null=False, blank=False)
    telegram = models.CharField("Telegram username", null=True, blank=True, max_length=70)
    extra_contact = models.CharField("Qo'shimcha Contact", null=True, blank=True, max_length=256)
    additional = models.TextField("Qiziqishingiz haqida qisqacha", null=True, blank=True)
    via = models.CharField(max_length=128, blank=True, null=True, default="Aniq emas")
    view = models.BooleanField(default=False)
    contacted = models.BooleanField(default=False)
    who_contacted = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      limit_choices_to={'ut': 1})

    class Meta:
        verbose_name = "Yangi Yozilmoqchi"
        verbose_name_plural = "Kursga Yozilmoqchi bo'lganlar"

    def __str__(self):
        return f"{self.name} | {self.phone} | {self.contacted} "
