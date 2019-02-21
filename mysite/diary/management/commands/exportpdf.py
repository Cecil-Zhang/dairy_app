from django.core.management.base import BaseCommand, CommandError
from diary.models import Diary
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
        if options.get('all', False):
            years = Diary.objects.values_list('year', flat=True).distinct()
            for y in years:
                print(y)
                months = Diary.objects.filter(year=y).values_list('month', flat=True).distinct()
                for m in months:
                    diaries = get_month_diaries(y, m)
                    params = {
                        'diaries': diaries
                    }
                    path = 'diaries/year_{}/month_{}.pdf'.format(y, m)
                    Render.savePdf('diary/monthView.html', params, path)
                    print('Diaries export to ' + os.path.join(settings.BACKUP_ROOT, path))
        else:
            year = options.get('year')
            month = options.get('month')
            diaries = get_month_diaries(year, month)
            if not diaries:
                print('No diaries found in {}, {}'.format(month, year))
                return
            params = {
                'diaries': diaries
            }
            path = 'diaries/year_{}/month_{}.pdf'.format(diaries[0].year, diaries[0].month)
            Render.savePdf('diary/monthView.html', params, path)
            print('Diaries export to ' + os.path.join(settings.BACKUP_ROOT, path))