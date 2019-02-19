from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
import random, string

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    random_prefix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return 'diary/images/user_{}/{}_{}'.format(instance.diary.author.id, random_prefix, filename)

class Diary(models.Model):
    datetime = models.DateTimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    weather = models.CharField(null=True, max_length=20)
    title = models.CharField(null=True, max_length=30)
    content = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '<Diary: Dairy at {} >'.format(self.datetime.strftime("%Y-%m-%d"))

    def populateYMD(self):
        datetime = self.datetime
        if datetime is None:
            raise FieldDoesNotExist()
        self.year = datetime.year
        self.month = datetime.month
        self.day = datetime.day

class DiaryFile(models.Model):
    diary = models.ForeignKey(Diary, related_name='pictures', on_delete=models.CASCADE)
    file = models.FileField(upload_to = user_directory_path)