from django.db import models

# Create your models here.


class RegistroCotacao(models.Model):
    moeda_origem = models.CharField(max_length=5, default='USD')
    moeda_destino = models.CharField(max_length=5, default='BRL')
    valor = models.DecimalField(max_digits=10, decimal_places=4)
    data_hora_consulta = models.DateTimeField(auto_now_add=True)
    consulta_personalizada = models.BooleanField(default=False)
    data_consulta = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-data_hora_consulta', '-id']

    def __str__(self):
        return f'{self.moeda_origem}/{self.moeda_destino} = {self.valor}'
