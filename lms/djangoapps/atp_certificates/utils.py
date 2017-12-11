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

import logging
log = logging.getLogger(__name__)

def generate_html(user,score,course_img_path,template_path,course_title,categorie,certif_img_path,logo_path,theme_path,lang):
    log.info("generate_html start: "+str(datetime.datetime.now().strftime("%s")))
    date = str(datetime.datetime.today().strftime('%d/%m/%Y'))
    rendered_html = open('/edx/var/edxapp/media/certificates/template_'+lang+'.html','r').read()
    log.info("generate_html theme_path: "+course_img_path)
    rendered_html = rendered_html.replace("'+course_img_path+'",course_img_path.encode('utf-8'))
    rendered_html = rendered_html.replace("'+date+'",date.encode('utf-8'))
    log.info("generate_html theme_path: "+course_title)
    rendered_html = rendered_html.replace("'+course_title+'",course_title.encode('utf-8'))
    log.info("generate_html theme_path: "+categorie)
    rendered_html = rendered_html.replace("'+categorie+'",categorie.encode('utf-8'))
    log.info("generate_html theme_path: "+user)
    rendered_html = rendered_html.replace("'+user+'",user.encode('utf-8'))
    log.info("generate_html theme_path: "+score)
    rendered_html = rendered_html.replace("'+score+'",score.encode('utf-8'))
    log.info("generate_html theme_path: "+certif_img_path)
    rendered_html = rendered_html.replace("'+certif_img_path+'",certif_img_path.encode('utf-8'))
    log.info("generate_html theme_path: "+logo_path)
    rendered_html = rendered_html.replace("'+logo_path+'",logo_path.encode('utf-8'))
    log.info("generate_html theme_path: "+theme_path)
    rendered_html = rendered_html.replace("'+theme_path+'",theme_path.encode('utf-8'))
    result = StringIO.StringIO()
    log.info("certif pdf pisa start: "+str(datetime.datetime.now().strftime("%s")))
    pdf = pisa.pisaDocument(rendered_html, dest=result)
    log.info("certif pdf pisa end: "+str(datetime.datetime.now().strftime("%s")))
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
        log.info("generate_html Ok: "+str(datetime.datetime.now().strftime("%s")))
        return response
    log.info("generate_html Ko: "+str(datetime.datetime.now().strftime("%s")))
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
