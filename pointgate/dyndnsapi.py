from functools import wraps
import json

from flask import Blueprint, request, Response, current_app, abort
import requests
from requests.auth import HTTPBasicAuth


dyndnsapi = Blueprint('dyndnsapi', __name__)


# stolen straight from http://flask.pocoo.org/snippets/8/
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return (username == current_app.config['UPDATE_USER'] and
            password == current_app.config['UPDATE_PASSWORD'])


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@dyndnsapi.route('/nic/update')
@requires_auth
def update_record():
    auth = HTTPBasicAuth(current_app.config['POINTDNS_USER'],
                         current_app.config['POINTDNS_API_KEY'])
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }

    for field in ('hostname', 'myip'):
        if not field in request.args:
            abort(400, 'Missing mandatory field: {}'.format(field))

    # parse url arguments
    hostnames = request.args['hostname'].split(',')
    ip = request.args['myip']

    # list all zones
    api = current_app.config['POINTDNS_API_URL']
    r = requests.get('{}/zones'.format(api),
                     headers=headers,
                     auth=auth)
    try:
        r.raise_for_status()

        for z in r.json():
            zone = z['zone']
            if zone['name'] in hostnames:
                fqdn = '{}.'.format(zone['name'])
                rec = {
                    'zone_record': {
                        'record_type': 'A',
                        'name': fqdn,
                        'data': ip,
                        'ttl': current_app.config['POINTDNS_RECORD_TTL'],
                    }
                }

                records_url = '{}/zones/{}/records'.format(api, zone['id'])

                # found our zone, get all records
                record_id = None
                r = requests.get(records_url,
                                 headers=headers,
                                 auth=auth)
                r.raise_for_status()

                for rec in r.json():
                    record = rec['zone_record']

                    if record['record_type'] == 'A' and record['name'] == fqdn:
                        record_id = record['id']
                        break

                if record_id is None:
                    # create new if not present
                    r = requests.post(records_url,
                                      data=json.dumps(rec),
                                      headers=headers,
                                      auth=auth)
                else:
                    # update old record
                    r = requests.put('{}/{}'.format(records_url, record_id),
                                     data=json.dumps(
                                         {'zone_record': {'data': ip}}
                                     ),
                                     headers=headers,
                                     auth=auth)
                print r.text
                r.raise_for_status()
                print('{} {}({}) -> {}. Reponse: {}'.format(
                      'Created' if record_id is None else 'Updated',
                      fqdn, zone['id'], ip,
                      r.status_code))
    except requests.HTTPError as e:
        print(e)  # just print to logs, do not disclose information to the
                  # outside
        abort(500, 'Error while communicating with PointDNS. Status: {}'
              .format(e.status_code))

    return 'hostnames: {}\nip: {}'.format(hostnames, ip)
