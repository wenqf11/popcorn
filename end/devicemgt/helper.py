__author__ = 'LY'

import settings

def handle_uploaded_file(username, f):
    print f.name.split('.')[-1]
    path = settings.IMG_DIR+'/'+username+'.'+f.name.split('.')[-1]
    print path
    with open(path, 'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
    return path