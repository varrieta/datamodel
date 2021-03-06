import json
import time
import httplib
import os
from subprocess import call

# Exit if we are not on origin/master
if os.environ['TRAVIS_SECURE_ENV_VARS'] == 'true' and os.environ['TRAVIS_BRANCH'] == 'master':
    with open('/tmp/template_db.dump', 'w') as f:
        call(['pg_dump', '-n', '"qgep"', '-Fc', 'qgep'], stdout=f)

    # Release name based on date/time
    releasename=time.strftime("%Y%m%d-%H%M%S")

    # Create a release
    conn = httplib.HTTPSConnection('api.github.com')
    headers = {
      'User-Agent' : 'Deploy-Script',
      'Authorization': 'token {}'.format(os.environ['OAUTH_TOKEN'])
    }
    data = json.dumps({"tag_name": releasename})

    conn.request('POST', '/repos/QGEP/datamodel/releases', body=data, headers=headers)

    response = conn.getresponse()

    release = json.load(response)

    print release


    conn = httplib.HTTPSConnection('uploads.github.com')
    headers['Content-Type'] = 'application/zip'
    url='{}?name={}'.format(release['upload_url'][:-13], 'template_db.dump')
    print 'Upload to ' + url

    with open('/tmp/template_db.dump', 'r') as f:
        conn.request('POST', url, f, headers)

    print conn.getresponse().read()
