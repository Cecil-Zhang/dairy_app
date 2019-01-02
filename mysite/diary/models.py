from django.db import models

class Diary(models.Model):
    datetime = models.DateTimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    weather = models.CharField(max_length=20)
    content = models.TextField(null=True)

    def __str__(self):
        return '<Diary: Dairy at {} >'.format(self.datetime.strftime("%Y-%m-%d"))