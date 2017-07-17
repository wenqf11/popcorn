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

def get_devices_by_user_class(classes, parentid):
    devices_list = list()
    devices = k_device.objects.filter(classid_id=parentid)
    devices_list.extend(queryset2list(devices))
    for _c in classes:
        if _c.parentid == parentid:
            tmp_list = get_devices_by_user_class(classes, _c.id)
            devices_list.extend(tmp_list)

    return devices_list

def queryset2list(queryset):
    res = list()
    for q in queryset:
        res.append(q)
    return res

@login_required
def print_qrcode(request):
    user = k_user.objects.get(username=request.user.username)
    data = dict()
    devicetype = dict()
    devicenum = dict()
    _classid = user.classid_id
    classes = k_class.objects.all()
    _devices = list()
    _devices.extend(get_devices_by_user_class(classes, _classid))
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
    server_msg = 'QRCode Error!'
    path = settings.WEBSET_ROOT_PATH+settings.MEDIA_URL
    path = os.path.join(path,'qrcode/')
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
        fpath = path+'qrcode.zip'
        archive = zipfile.ZipFile(fpath, 'w')
        ori_path = os.getcwd()
        os.chdir(path)
        for _f in filelist:
            filename = gen_qrcode(path, _f)
            archive.write(filename)
        os.chdir(ori_path)
        archive.close()
        return HttpResponse(json.dumps({
            "link": "/static/images/qrcode/qrcode.zip"
            }), content_type="application/json")
    return HttpResponse(json.dumps({
        "username": user.username,
        "server_msg":server_msg
        }), content_type="application/json")



def gen_qrcode(path, filename):
    try:
        img = qrcode.make(filename)
        img.save(path+filename+'.png')
    except Exception as e:
        with open('error.txt', 'w') as fd:
            fd.write('{}\n'.format(str(e)))
            fd.write(path+filename+'.png\n')
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
