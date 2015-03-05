import flask
import mysql.connector
from acitoolkit.acitoolkitlib import Credentials
from aciconfigdb import ConfigDB
from subprocess import call

global cdb

description = 'Simple set of visualization examples.'
creds = Credentials('', description)
args = creds.get()

app = flask.Flask(__name__)

@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    table_data = cdb.get_versions()
    return flask.render_template('index.html',
                                 table_data=table_data)


@app.route('/diffs')
def diffs():
    table_data = cdb.get_versions()
    ver1 = flask.request.args.get('ver1')
    ver2 = flask.request.args.get('ver2')
    diff_file = flask.request.args.get('file')
    if ver1:
        filenames=cdb.get_filenames(ver1)
    else:
        filenames=None
    diffs = {}
    if filenames is not None:
        for filename in filenames:
            diffs[filename] = cdb.has_diffs(ver1, ver2, filename)
    if diff_file:
        cdb.sdiff(ver1, ver2, diff_file)
    return flask.render_template('diffs.html',
                                 ver1=ver1,
                                 ver2=ver2,
                                 table_data=table_data,
                                 filenames=filenames,
                                 diffs=diffs)
    
@app.route('/snapshot')
def snapshot():
    """ Displays the index page accessible at '/snapshot'
    """
    cdb.take_snapshot()
    return flask.redirect(flask.url_for('index'))

@app.route('/rollback')
def rollback():
    table_data = cdb.get_versions()
    version = flask.request.args.get('version')
    rollback_files = flask.request.args.getlist('file')
    if version:
        filenames=cdb.get_filenames(version)
    else:
        filenames=None
    if rollback_files:
        cdb.rollback(version, rollback_files)
    return flask.render_template('rollback.html',
                                 version=version,
                                 table_data=table_data,
                                 filenames=filenames)
class Args(object):
    def __init__(self):
        self.url = None
        self.login = None
        self.password = None

if __name__ == '__main__':
    args = Args()
    args.url = ''
    args.login = ''
    args.password = ''
    
    cdb = ConfigDB(args)
    app.run(debug=True)
