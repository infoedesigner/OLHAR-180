from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField('Ativo', default=True, blank=True)
    created = models.DateTimeField('Criado', auto_now_add=True)
    modified = models.DateTimeField('Modificado', auto_now=True)

    class Meta:
        abstract = True


class State(BaseModel):

    name = models.CharField('Nome', max_length=40)
    abbreviation = models.CharField('Sigla', max_length=2)
    territory_id = models.CharField('Id do Território', unique=True, max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='Estado'
        verbose_name_plural = 'Estados'
        ordering = ['name']


class Bank(BaseModel):

    name = models.CharField('Nome', max_length=100)
    code = models.CharField('Sigla', max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['code']


class City(BaseModel):

    name = models.CharField('Nome', max_length=100)
    state = models.CharField('Estado', max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name ='Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['state', 'name']
