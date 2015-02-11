#!/usr/bin/python

import dominate
import requests
import warnings

from dominate import document
from dominate.tags import *

warnings.filterwarnings("ignore")

doc = dominate.document(title='Sesiones')


urls = [
        'https://domain.tld/sessioncounter',
	]

results = []

with doc.head:
    body(onload='JavaScript:timedRefresh(2000);')
    script(type='text/javascript', src='https://static.uchile.cl/demre/asistente/refresh.js')
    link(rel='stylesheet', href='http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css')
    link(rel='stylesheet', href='http://maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css')
    script(type='text/javascript', src='http://code.jquery.com/jquery-1.10.2.min.js')
    script(type='text/javascript', src='http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js')
    
    
with doc:
    div(cls='container')
    h1('Sesiones')
    div(cls='page-header')
    for url in urls:
        result = requests.get(url, verify=False)
        results.append(result)
        div(img(src='http://dummyimage.com/230x100/000/fff&text=' + result.text, _class='thumbnail img-responsive'), _class='col-md-4')

with open('index.html', 'w') as f:
    f.write(doc.render())


