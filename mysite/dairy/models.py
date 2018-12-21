from django.db import models

class Dairy(models.Model):
    datetime = models.DateTimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    weather = models.CharField(max_length=20)
    content = models.TextField(null=True)

    def __str__(self):
        return '<Dairy: Dairy at {} >'.format(self.datetime.strftime("%Y-%m-%d"))