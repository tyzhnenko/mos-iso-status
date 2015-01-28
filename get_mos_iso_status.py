import requests
import pymongo
from jenkinsapi.jenkins import Jenkins
from jenkinsapi import api


FUEL_URL = 'http://jenkins-product.srt.mirantis.net:8080/'
FUEL_RELEASES = ['6.0', '6.1']
N = 10  # script will update only last N+1 results

jenkins = Jenkins(FUEL_URL, username=None, password=None)
connection = pymongo.Connection()                                               
mos = connection['MOS']

images = list(mos.images.find())
if len(images) > 0:
    OLD_RESULTS = images[0]

RESULTS = {}


for release in FUEL_RELEASES:
    job_name = '{0}.all'.format(release)
    fjob_name = job_name.replace('.', '_')
    jenkins_job = jenkins[job_name]

    if fjob_name not in OLD_RESULTS:
        OLD_RESULTS[fjob_name] = {}
    if 'builds' not in OLS_RESULTS[fjob_name]:
        OLD_RESULTS[fjob_name]['builds'] = []
    RESULTS[fjob_name] = {}
    RESULTS[fjob_name]['builds'] = []

    RESULTS[fjob_name]['test_groups'] = jenkins_job.get_downstream_job_names()

    latest_build = jenkins_job.get_last_buildnumber()

    for n in OLD_RESULTS[fjob_name]['builds']:
        if n['build_number'] < latest_build - N:
            RESULTS[fjob_name]['builds'].append(n)

    for n in xrange(latest_build - N, latest_build + 1):
        try:
            build = jenkins_job.get_build(n)
            date = str(build.get_timestamp()).split('+')[0]
            status = build.get_status() or 'IN PROGRESS'
            iso_link, torrent_link = '', ''

            for art in build.get_artifacts():
                if 'iso.data.txt' in art.url:
                    data = requests.get(art.url).text.encode('ascii')
                    for line in data.split('\n'):
                        if 'HTTP_LINK' in line:
                            iso_link = line.split('=')[1]
                        elif 'HTTP_TORRENT' in line:
                            torrent_link = line.split('=')[1]

            RESULTS[fjob_name]['builds'].append({'build_number': n,
                                                 'build_status': status,
                                                 'tests': {}, 'date': date,
                                                 'iso_link': iso_link,
                                                 'torrent_link': torrent_link})

            print "Synced results from iso build job", n
        except:
            print "Can't get info about build", n

    for test in RESULTS[fjob_name]['test_groups']:
        test_job = jenkins[test]
        latest_test_build = test_job.get_last_buildnumber()
        for j in xrange(latest_test_build - N, latest_test_build + 1):
            try:
                build = test_job.get_build(j)
                r = build.get_upstream_build_number()
                status = build.get_status() or 'IN PROGRESS'

                for result in RESULTS[fjob_name]['builds']:
                    if result['build_number'] == r:
                        result['tests'][test.replace('.', '_')] = status

                print "Synced results from iso testing job", j
            except:
                print "Can't get info about test build", j


mos.images.drop()
mos.images.insert(RESULTS)
