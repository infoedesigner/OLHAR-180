from django.db import models

from nxt.core.models import BaseModel


class Execution(BaseModel):

    crawler = models.CharField('Nome do Crawler', max_length=30)
    finish = models.DateTimeField('Finalizado', null=True, blank=True)
    status = models.CharField('Situação', max_length=30)
    error_details = models.TextField('Detalhes de Erro', blank=True)
    log = models.TextField('Log', blank=True)

    def __str__(self):
        return f'[{self.created}] {self.crawler}'

    class Meta:
        verbose_name = 'Execução'
        verbose_name_plural = 'Execuções'
        ordering = ['-created']
