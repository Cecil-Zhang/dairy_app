from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings
import os

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), response, encoding='UTF-8', link_callback=link_callback)

        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    def savePdf(path: str, params: dict, filepath):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        filepath = os.path.join(settings.BACKUP_ROOT, filepath)
        os.makedirs(filepath[:filepath.rfind('/')], exist_ok=True)
        file = open(filepath, 'w+b')
        pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), file, encoding='UTF-8', link_callback=link_callback)

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    print('link_callback({}, {})'.format(uri, rel))
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)
    # make sure that file exists
    if not os.path.isfile(path):
        msg = '{} not found, media URI must start with {} or {}'.format(path, sUrl, mUrl)
        raise Exception(
            msg
        )
    return path


