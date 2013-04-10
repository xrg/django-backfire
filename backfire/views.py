# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders

from Backfire import *

def _get_file_path( url ):
    path = urlparse(url).path
    if path.startswith(settings.STATIC_URL):
        path = path[len(settings.STATIC_URL):]
        res = finders.find(path, all=False)
        if res:
            return res
    # don't accept any path elements from the remote side, they could
    # be dangerous.
    return settings.STATIC_ROOT + path.rsplit('/', 1)[-1]
    
def cssLoader( url ):
    f = open( _get_file_path(url) , 'r')
    content = f.read()
    f.close()
    return content
    
def cssSaver(uri, contents):
    try:
        f = open( _get_file_path(uri) , 'w')
        f.write(contents)
        f.close()
        return True
    except Exception:
        return False

@staff_member_required
def get_respond(request):
    if request.method == "POST":
        changes = request.POST.get("backfire-changes", False)
        try:
            if changes:
                result = process(changes, cssLoader, cssSaver )
                return HttpResponse(create_message_for_client( result ))
        except Exception, e:
            log("Exception: %s" % e)
    return HttpResponse(create_message_for_client( ACCESS_GRANTED ))
