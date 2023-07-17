from django.db import models


class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Todo(AbstractModel):
    content = models.CharField(max_length=200, null=False, blank=False, verbose_name="Описание")
    details = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Детальное описание")
    status = models.ForeignKey('webapp.Status', related_name='status', null=True, blank=True, on_delete=models.PROTECT,
                                verbose_name='Статус')
    types = models.ManyToManyField('webapp.Type', related_name='types', blank=True)
    project = models.ForeignKey('webapp.Project', related_name='projects', default='1', verbose_name='Проект',
                                 on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.pk} {self.content} ({self.types.all()}): {self.status}"

    class Meta:
        db_table = "To-Do list"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Status(AbstractModel):
    name = models.CharField(max_length=35, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "status"
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(AbstractModel):
    name = models.CharField(max_length=35, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "types"
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Project(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(max_length=2000, verbose_name='Описание')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'project'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
