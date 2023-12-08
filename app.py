import requests
import argparse
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_openshift_versions(channel, version):
    url = f'https://api.openshift.com/api/upgrades_info/graph?channel={channel}-{version}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            json_data = response.json()

            openshift_versions = json_data.get('nodes', [])
            openshift_versions = [node.get('version', '') for node in openshift_versions if version in node.get('version', '')]

            return openshift_versions
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/api/upgrades_info', methods=['GET'])
def api_upgrades_info():

    channel = request.args.get('channel')
    version = request.args.get('version')


    if not channel or not version:
        print("Missing parameters")
        return jsonify(error='Both channel and version must be provided'), 400


    openshift_versions = get_openshift_versions(channel, version)


    print(f"OpenShift versions: {openshift_versions}")

    if openshift_versions:
        return jsonify(openshift_versions)
    else:
        print("No OpenShift versions found")
        return jsonify(error='No OpenShift versions found'), 400

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get OpenShift channel information.')
    parser.add_argument('--api', action='store_true', help='Start Flask app for OpenShift upgrades API')
    parser.add_argument('--version', help='The OpenShift version')
    parser.add_argument('--channel', help='stable, fast, candidate')


    args = parser.parse_args()

    if args.api:
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        if not args.version and not args.channel:
            parser.error('Either --version or --channel must be provided.')

        openshift_versions = get_openshift_versions(args.channel, args.version)

        for version in openshift_versions:
            print(version)