#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weasyprint import HTML
import codecs
from django.template import Context, Template
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from cgi import escape
from edxmako.shortcuts import render_to_response,render_to_string
from django.views.generic import TemplateView
import datetime

def generate_html(user,score,course_img_path,template_path,course_title,categorie):
    date = str(datetime.datetime.today().strftime('%d/%m/%Y'))
    rendered_html = open('/edx/var/edxapp/media/certificates/template.html','r').read()
    rendered_html = rendered_html.replace("'+course_img_path+'",course_img_path.encode('utf-8'))
    rendered_html = rendered_html.replace("'+date+'",date.encode('utf-8'))
    rendered_html = rendered_html.replace("'+course_title+'",course_title.encode('utf-8'))
    rendered_html = rendered_html.replace("'+categorie+'",categorie.encode('utf-8'))
    rendered_html = rendered_html.replace("'+user+'",user.encode('utf-8'))
    rendered_html = rendered_html.replace("'+score+'",score.encode('utf-8'))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(rendered_html, dest=result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
