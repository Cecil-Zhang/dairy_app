from django.core.management.base import BaseCommand, CommandError
from diary.models import Diary
from django.contrib.auth.models import User
from diary.views import get_month_diaries
from diary.render import Render
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'export all diaries in a month to pdf, default to export last month'
    def add_arguments(self, parser):
        parser.add_argument('-Y', '--year', help='The year to export',)
        parser.add_argument('-M', '--month', help='The month to export',)
        parser.add_argument('--all', action='store_true', dest='all', help='Export all diaries',)

    def handle(self, *args, **options):
        users = User.objects.values_list('id', flat=True).distinct()
        if options.get('all', False):
            for u in users:
                years = Diary.objects.values_list('year', flat=True).distinct()
                for y in years:
                    months = Diary.objects.filter(author=u, year=y).values_list('month', flat=True).distinct()
                    for m in months:
                        diaries = get_month_diaries(u, y, m)
                        params = {
                            'diaries': diaries
                        }
                        path = 'diaries/user_{}/year_{}/month_{}.pdf'.format(u, y, m)
                        Render.savePdf('diary/monthView.html', params, path)
                        print('Diaries export to ' + os.path.join(settings.BACKUP_ROOT, path))
        else:
            for u in users:
                year = options.get('year')
                month = options.get('month')
                diaries = get_month_diaries(u, year, month)
                if not diaries:
                    print('No diaries found in {}, {} for user:{}'.format(month, year, u))
                else:
                    params = {
                        'diaries': diaries
                    }
                    path = 'diaries/user_{}/year_{}/month_{}.pdf'.format(u, diaries[0].year, diaries[0].month)
                    Render.savePdf('diary/monthView.html', params, path)
                    print('Diaries export to ' + os.path.join(settings.BACKUP_ROOT, path))