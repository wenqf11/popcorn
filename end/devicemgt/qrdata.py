# -*- encoding=UTF-8 -*-
__author__ = 'LY'

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import *
from views import get_purviews_and_render_to_response
import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import json
import qrcode
import StringIO

@login_required
def print_qrcode(request):
    user = k_user.objects.get(username=request.user.username)
    data = dict()
    devicetype = dict()
    devicenum = dict()
    _classid = user.classid
    _devices = k_device.objects.filter(classid_id=_classid)
    data["devicetypes"] = dict()
    for _d in _devices:
        if not devicetype.has_key(_d.typeid_id):
            devicetype[_d.typeid_id] = list()
            devicenum[_d.typeid_id] = 0
        devicetype[_d.typeid_id].append({
                                            "name":_d.brief,
                                            "id": devicenum[_d.typeid_id]+1})
        devicenum[_d.typeid_id] += 1
    for (k,v) in devicetype.items():
        _name = k_devicetype.objects.filter(id=k)
        if len(_name) == 1:
            _name = _name[0].name
            data["devicetypes"][_name] = v

    variables = RequestContext(request, {'username':user.username, 'useravatar': user.avatar, 'data':data})
    return get_purviews_and_render_to_response(request.user.username, 'print_qrcode.html', variables)


def download_qrcode(request):
    user = k_user.objects.get(username=request.user.username)
    server_msg = ''
    path = './static/images/qrcode/'
    if request.method == "POST":
        filelist = request.POST.getlist("filelist[]")
        '''elegant way but doesn't work yet
        #temp = tempfile.TemporaryFile()
        # s = StringIO.StringIO()
        # archive = zipfile.ZipFile(s, 'w')
        # for _f in filelist:
        #     filename = gen_qrcode(path, _f)
        #     #archive.write(path+filename)
        #     archive.write('logo.png')
        # archive.close()
        # wrapper = s.getvalue()#FileWrapper(temp)
        # response = HttpResponse(wrapper, content_type='application/x-zip-compressed')
        # response['Content-Disposition'] = 'attachment;filename=qrcode.zip'
        # response['Content-Length'] = s.tell()#temp.tell()
        # #print s.tell()
        # #temp.seek(0)
        #
        # return response
        '''
        ''' Not elegant but ok
       '''
        archive = zipfile.ZipFile(path+'qrcode.zip', 'w')
        for _f in filelist:
            filename = gen_qrcode(path, _f)
            archive.write(path+filename)
        archive.close()
        return HttpResponse(json.dumps({
            "link": "/static/images/qrcode/qrcode.zip"
            }), content_type="application/json")
    return HttpResponse(json.dumps({
        "username": user.username,
        "server_msg":server_msg
        }), content_type="application/json")



def gen_qrcode(path, filename):
    img = qrcode.make(filename)
    img.save(path+filename+'.png')
    return filename+'.png'


def send_file(request):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    filename = 'logo.png' # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def send_zipfile(request):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(10):
        filename = __file__ # Select your files here.
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response