import errno
import os
import re

from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from edxmako.shortcuts import render_to_response, render_to_string
from util.json_request import  JsonResponse, JsonResponseBadRequest

from organizations.models import Organization
from microsite_configuration.models import (
    Microsite,
    MicrositeOrganizationMapping,
    MicrositeTemplate
)

from .models import MicrositeDetail, MongoMicrosites


@login_required
def create_microsite(request):

    microsite_details = {}
    microsite_details['name'] = request.POST['display_name']
    microsite_details['primary_color'] = request.POST['primary_color']
    microsite_details['color'] = '#000000'
    microsite_details['secondary_color'] = request.POST['secondary_color']
    microsite_details['logo'] = request.FILES['logo']
    microsite_details['language_code'] = request.POST['language']

    if validate_data(microsite_details):
        details_status = MicrositeDetail.save_details(microsite_details)
        if details_status['success'] == True:
            microsite_url = launch_microsite(request, microsite_details)
            return JsonResponse({
                'url': '/home'
            })
        else:
            return JsonResponseBadRequest({
                "ErrMsg": _(details_status['error_msg'])
            })
    else:
        return JsonResponseBadRequest({
            "ErrMsg": _("Invalid Data. Please Enter valid Data.")
        })

@csrf_exempt
@login_required
def update_microsite(request, microsite_id=None):
    if request.method == 'GET':
        #try:
        microsite_details = MicrositeDetail.objects.get(id=microsite_id)
        microsite_name = microsite_details.name
        microsite = Microsite.objects.get(key=microsite_name)
        microsite_value = microsite.values
        lang_key = 0
        logo_key = 0
        primary_key = 0
        secondary_key = 0
        i = 0
        for n in microsite_value:
            if n == 'language_code':
                lang_key = i
            if n == 'logo':
                logo_key = i
            if n == 'primary_color':
                primary_key = i
            if n == 'secondary_color':
                secondary_key = i
            i = i + 1
        primary_color = microsite_value.values()[primary_key]
        secondary_color = microsite_value.values()[secondary_key]
        logo = microsite_value.values()[logo_key]
        language_code = microsite_value.values()[lang_key]
        context = {}
        context['primary_color'] = primary_color
        context['secondary_color'] = secondary_color
        context['key'] = microsite_name
        context['logo_site'] = logo
        context['language_code'] = language_code
        context['microsite_value'] = microsite_value
        return render_to_response('update-microsite.html',context)

    elif request.method == 'POST':
        context = {}
        #try:
        # GET request params
        try:
            microsite_logo = request.FILES['logo']
        except:
            microsite_logo = ''
        key = request.POST['key']
        primary_color = request.POST['primary_color']
        secondary_color = request.POST['secondary_color']
        language_code = request.POST['language_code']
        #get microsite infos
        microsite_details = MicrositeDetail.objects.get(id=microsite_id)
        microsite_name = microsite_details.name
        microsite = Microsite.objects.get(key=microsite_name)
        microsite_value = microsite.values
        lang_key = 0
        primary_key = 0
        secondary_key = 0
        i = 0
        for n in microsite_value:
            if n == 'language_code':
                lang_key = i
            elif n == 'primary_color':
                primary_key = i
            elif n == 'secondary_color':
                secondary_key = i
            i = i + 1
        current_primary_color = microsite_value.values()[primary_key]
        current_secondary_color = microsite_value.values()[secondary_key]
        current_language_code = microsite_value.values()[lang_key]
        #update microsite_info
        if key or key != '':
            microsite_name = key
        if not primary_color or primary_color == '':
            primary_color = current_primary_color
        if not secondary_color or secondary_color == '':
            secondary_color = current_secondary_color
        if not language_code or language_code == '':
            language_code = current_language_code
        microsite_logo_name = ''
        if microsite_logo or microsite_logo != '':
            microsite_logo_path = "/edx/var/edxapp/media/microsite/"+microsite_name+"/images/"+microsite_logo.name
            with open(microsite_logo_path, 'wb+') as destination:
                for chunk in microsite_logo.chunks():
                    destination.write(chunk)
            microsite_logo_name = microsite_logo.name
            context['logo'] = True
        else:
            context['logo'] = False
        # Create microsite directory with css, logo and a template
        microsite_css_path = "/edx/var/edxapp/media/microsite/{name}/css/style.css".format(
            name=microsite_name
        )
        microsite_css_nav_path = "/edx/var/edxapp/media/microsite/{name}/css/nav.css".format(
            name=microsite_name
        )
        microsite_css_dashboard_path = "/edx/var/edxapp/media/microsite/{name}/css/dashboard.css".format(
            name=microsite_name
        )
        microsite_css_course_about_path = "/edx/var/edxapp/media/microsite/{name}/css/course_about.css".format(
            name=microsite_name
        )
        microsite_css_courseware_path = "/edx/var/edxapp/media/microsite/{name}/css/courseware.css".format(
            name=microsite_name
        )
        microsite_css_stat_dashboard_path = "/edx/var/edxapp/media/microsite/{name}/css/stat_dashboard.css".format(
            name=microsite_name
        )
        microsite_css_footer_path = "/edx/var/edxapp/media/microsite/{name}/css/footer.css".format(
            name=microsite_name
        )
        microsite_css_main_path = "/edx/var/edxapp/media/microsite/{name}/css/main.css".format(
            name=microsite_name
        )
        microsite_logo_path = "/edx/var/edxapp/media/microsite/{name}/images/{logo_name}".format(
            name=microsite_name,
            logo_name=microsite_logo.name
        )
        mother_domain = settings.SITE_NAME
        cookie_domain = '.'+mother_domain
        site_name = microsite_name + '.' + mother_domain
        if microsite_logo or microsite_logo != '':
            logo_value_path = "/media/microsite/"+microsite_name+"/images/"+microsite_logo_name
        else:
            logo_value_path = microsite_value.values()[5]
        values_save = {
          "domain_prefix":microsite_name,
          "university":microsite_name,
          "platform_name":microsite_name,
          "logo":logo_value_path,
          "ENABLE_MKTG_SITE":False,
          "SITE_NAME":site_name,
          "course_org_filter":microsite_name,
          "course_about_show_social_links":False,
          "css_overrides_file":"/media/microsite/"+microsite_name+"/css/style.css",
          "css_overrides_nav":"/media/microsite/"+microsite_name+"/css/nav.css",
          "css_overrides_dashboard":"/media/microsite/"+microsite_name+"/css/dashboard.css",
          "css_overrides_course_about":"/media/microsite/"+microsite_name+"/css/course_about.css",
          "css_overrides_courseware":"/media/microsite/"+microsite_name+"/css/courseware.css",
          "css_overrides_stat_dashboard":"/media/microsite/"+microsite_name+"/css/stat_dashboard.css",
          "css_overrides_footer":"/media/microsite/"+microsite_name+"/css/footer.css",
          "css_overrides_main":"/media/microsite/"+microsite_name+"/css/main.css",
          "primary_color":primary_color,
          "secondary_color":secondary_color,
          "show_partners":False,
          "show_homepage_promo_video":False,
          "course_index_overlay_text":"Bienvenue sur "+microsite_name,
          "homepage_overlay_html":"<h1>"+microsite_name+"</h1>",
          "favicon_path":logo_value_path,
          "ENABLE_THIRD_PARTY_AUTH":False,
          "ALLOW_AUTOMATED_SIGNUPS":True,
          "ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER":True,
          "course_email_from_addr":"ne-pas-repondre@themoocagency.com",
          "SESSION_COOKIE_DOMAIN":cookie_domain,
          "language_code":language_code
        }
        context['microsite_logo_name'] = microsite_logo_name
        context['primary_color'] = primary_color
        context['secondary_color'] = secondary_color
        context['logo_value_path'] = logo_value_path
        context['language_code'] = language_code
        context['values'] = values_save
        if key != microsite_name and key != '' and key:
            microsite.key = key
            site, created = Site.objects.get_or_create(
                domain=site_name,
                name=microsite_name.capitalize()
            )
            microsite.site = site
        microsite.key = microsite_name
        microsite.values = values_save
        microsite.save()
        css_path = [microsite_css_nav_path,microsite_css_dashboard_path,microsite_css_course_about_path,microsite_css_courseware_path,microsite_css_stat_dashboard_path,microsite_css_footer_path,microsite_css_main_path]
        for n in css_path:
            if not os.path.exists(os.path.dirname(n)):
                try:
                    os.makedirs(os.path.dirname(n))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(n, "w") as f:
                template = n.split('/')
                l = len(template) - 1
                template_name = 'microsite_manager/'+template[l].replace('.css','.txt')
                css_content = render_to_string(
                    template_name,
                    {
                        'atp_primary_color': primary_color,
                        'atp_secondary_color': secondary_color,
                        'font_family': 'mywebfont',
                        'banner_image': 'banner_image',
                    },
                    request=request
                )
                f.write(css_content)
        if microsite_name:
            try:
                os.makedirs(os.path.dirname(microsite_logo_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        try:
            with open(microsite_logo_path, 'wb+') as destination:
                for chunk in microsite_logo.chunks():
                    destination.write(chunk)
            #update microsite details
            microsite_details = MicrositeDetail.objects.get(name=microsite_name)
            microsite_details.logo = microsite_logo.name
            microsite_details.language_code = language_code
            microsite_details.save()
        except:
            context['logo_status'] = 'no logo'

        return JsonResponse(context)

def launch_microsite(request, microsite_details):
        # Set the mother domain name
        mother_domain = settings.SITE_NAME

        # Get the require parameters
        microsite_name = microsite_details.get('name')
        primary_color = microsite_details.get('primary_color')
        secondary_color = microsite_details.get('secondary_color')
        microsite_logo = microsite_details.get('logo')
        language_code = microsite_details.get('language_code')


        # Create site
        site_name = microsite_name + '.' + mother_domain

        site, created = Site.objects.get_or_create(
            domain=site_name,
            name=microsite_name.capitalize()
        )

        cookie_domain = '.'+mother_domain
        # Create microsite using Database backend
        microsite = Microsite.objects.create(
            site=site,
            key=microsite_name,

            values = {
              "domain_prefix":microsite_name,
              "university":microsite_name,
              "platform_name":microsite_name,
              "logo":"/media/microsite/"+microsite_name+"/images/logo.png",
              "ENABLE_MKTG_SITE":False,
              "SITE_NAME":site_name,
              "course_org_filter":microsite_name,
              "course_about_show_social_links":False,
              "css_overrides_file":"/media/microsite/"+microsite_name+"/css/style.css",
              "css_overrides_nav":"/media/microsite/"+microsite_name+"/css/nav.css",
              "css_overrides_dashboard":"/media/microsite/"+microsite_name+"/css/dashboard.css",
              "css_overrides_course_about":"/media/microsite/"+microsite_name+"/css/course_about.css",
              "css_overrides_courseware":"/media/microsite/"+microsite_name+"/css/courseware.css",
              "css_overrides_stat_dashboard":"/media/microsite/"+microsite_name+"/css/stat_dashboard.css",
              "css_overrides_footer":"/media/microsite/"+microsite_name+"/css/footer.css",
              "css_overrides_main":"/media/microsite/"+microsite_name+"/css/main.css",
              "primary_color":primary_color,
              "secondary_color":secondary_color,
              "show_partners":False,
              "show_homepage_promo_video":False,
              "course_index_overlay_text":"Bienvenue sur "+microsite_name,
              "homepage_overlay_html":"<h1>"+microsite_name+"</h1>",
              "favicon_path":"/media/microsite/"+microsite_name+"/images/"+microsite_logo.name,
              "ENABLE_THIRD_PARTY_AUTH":False,
              "ALLOW_AUTOMATED_SIGNUPS":True,
              "ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER":True,
              "course_email_from_addr":"ne-pas-repondre@themoocagency.com",
              "SESSION_COOKIE_DOMAIN":cookie_domain,
              "language_code":language_code
            }
        )

        # Create organization

        organization, created = Organization.objects.get_or_create(
            name=microsite_name,
            short_name=microsite_name,
            active=True
        )

        # Create organization - microstite mapping
        organization_microsite_mapping = MicrositeOrganizationMapping.objects.create(
            organization=organization.name,
            microsite=microsite
        )
        # Create microsite directory with css, logo and a template

        microsite_css_path = "/edx/var/edxapp/media/microsite/{name}/css/style.css".format(
            name=microsite_name
        )
        microsite_css_nav_path = "/edx/var/edxapp/media/microsite/{name}/css/nav.css".format(
            name=microsite_name
        )
        microsite_css_dashboard_path = "/edx/var/edxapp/media/microsite/{name}/css/dashboard.css".format(
            name=microsite_name
        )
        microsite_css_course_about_path = "/edx/var/edxapp/media/microsite/{name}/css/course_about.css".format(
            name=microsite_name
        )
        microsite_css_courseware_path = "/edx/var/edxapp/media/microsite/{name}/css/courseware.css".format(
            name=microsite_name
        )
        microsite_css_stat_dashboard_path = "/edx/var/edxapp/media/microsite/{name}/css/stat_dashboard.css".format(
            name=microsite_name
        )
        microsite_css_footer_path = "/edx/var/edxapp/media/microsite/{name}/css/footer.css".format(
            name=microsite_name
        )
        microsite_css_main_path = "/edx/var/edxapp/media/microsite/{name}/css/main.css".format(
            name=microsite_name
        )
        microsite_logo_path = "/edx/var/edxapp/media/microsite/{name}/images/{logo_name}".format(
            name=microsite_name,
            logo_name=microsite_logo.name
        )
        css_path = [microsite_css_nav_path,microsite_css_dashboard_path,microsite_css_course_about_path,microsite_css_courseware_path,microsite_css_stat_dashboard_path,microsite_css_footer_path,microsite_css_main_path]
        for n in css_path:
            if not os.path.exists(os.path.dirname(n)):
                try:
                    os.makedirs(os.path.dirname(n))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(n, "w") as f:
                template = n.split('/')
                l = len(template) - 1
                template_name = 'microsite_manager/'+template[l].replace('.css','.txt')
                css_content = render_to_string(
                    template_name,
                    {
                        'atp_primary_color': primary_color,
                        'atp_secondary_color': secondary_color,
                        'font_family': 'mywebfont',
                        'banner_image': 'banner_image',
                    },
                    request=request
                )
                f.write(css_content)
        if not os.path.exists(os.path.dirname(microsite_logo_path)):

            try:
                os.makedirs(os.path.dirname(microsite_logo_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(microsite_logo_path, 'wb+') as destination:
            for chunk in microsite_logo.chunks():
                destination.write(chunk)

        return JsonResponse({'microsite':True})

def color_variation(color):
    '''
    ARG: color is code without '#'
    e.g. FF0000
    '''
    red = int(color[:2],16)
    green = int(color[2:4],16)
    blue = int(color[4:],16)
    return str((red, green, blue, 0.2)), str((red, green, blue, 0.5)), str((red, green, blue, 0.7))

def validate_data(microsite_details):
    re_for_color_code = '^#(?:[0-9a-fA-F]{3}){1,2}$'
    re_name = '^[a-zA-Z0-9-_]+$'
    match_color_code = re.search(re_for_color_code,microsite_details['color'])
    match_name = re.search(re_name, microsite_details['name'])
    if microsite_details['logo'] != '':
        logo_ext = microsite_details['logo'].name.lower().endswith(('.png', '.jpg', '.jpeg'))
    else:
        logo_ext = True
    if match_color_code and logo_ext and match_name:
        return True
    else:
        return False

def static_content(request,microsite_id):
    if len(MongoMicrosites.objects.filter(microsite_id=microsite_id)) != 0:
        microsite = MongoMicrosites.objects.get(microsite_id=microsite_id)
        return {'faq': microsite.faq,
                'tos': microsite.tos,
                'privacy':microsite.privacy,
                'honor': microsite.honor}
    else:
        return {'faq': 'Coming Soon',
                'tos': 'Coming Soon',
                'privacy':'Coming Soon',
                'honor': 'Coming Soon'}


@csrf_exempt
@require_POST
def add_microsite_content(request):
    microsite_id = request.POST['microsite_id']
    page_content = request.POST['microsite_content']
    page = request.POST['page']

    if len(MongoMicrosites.objects.filter(microsite_id=microsite_id)) != 0:
        microsite = MongoMicrosites.objects.get(microsite_id=microsite_id)
    else:
        microsite = MongoMicrosites(microsite_id=microsite_id)

    setattr(microsite, page, page_content)
    microsite.save()
    return JsonResponse({'content':getattr(microsite, page)})
