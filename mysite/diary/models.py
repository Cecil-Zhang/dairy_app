from django.db import models
from django.core.exceptions import FieldDoesNotExist

class Diary(models.Model):
    datetime = models.DateTimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    weather = models.CharField(max_length=20)
    content = models.TextField(null=True)

    def __str__(self):
        return '<Diary: Dairy at {} >'.format(self.datetime.strftime("%Y-%m-%d"))

    def populateYMD(self):
        datetime = self.datetime
        if datetime is None:
            raise FieldDoesNotExist()
        self.year = datetime.year
        self.month = datetime.month
        self.day = datetime.day