import json
import flask
import pymongo


app = flask.Flask(__name__)


@app.route('/')
def index_page():
    connection = pymongo.Connection()
    mos = connection['MOS']
    data = list(mos.images.find())[0]
    all_versions = []

    for k in data:
        if '_id' not in k:
            all_versions.append(k.replace('_', '.'))

    return flask.render_template("index.html", versions=all_versions)

@app.route('/mos/<version>')
def mos_images_status(version):
    ver = version.replace('.', '_')
    connection = pymongo.Connection()
    mos = connection['MOS']

    data = list(mos.images.find())[0]
    tests_types = data.get(ver, {}).get('test_groups', [])
    images = data.get(ver, {}).get('builds', [])
    images.reverse()

    return flask.render_template("iso_status.html", version=version,
                                 images=images, tests_types=tests_types)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080, threaded=True)
