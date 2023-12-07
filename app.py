import requests
import argparse
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_openshift_versions(channel, version):
    url = f'https://api.openshift.com/api/upgrades_info/graph?channel={channel}-{version}'

    try:
        # Make the HTTP request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()

            # Extract OpenShift versions
            openshift_versions = json_data.get('nodes', [])
            openshift_versions = [node.get('version', '') for node in openshift_versions if version in node.get('version', '')]

            return openshift_versions
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route('/api/upgrades_info', methods=['GET'])
def api_upgrades_info():
    # Get channel and version from query parameters
    channel = request.args.get('channel')
    version = request.args.get('version')

    # Check if both channel and version are provided
    if not channel or not version:
        print("Missing parameters")
        return jsonify(error='Both channel and version must be provided'), 400

    # Call the function with the provided arguments
    openshift_versions = get_openshift_versions(channel, version)

    # Debugging information
    print(f"OpenShift versions: {openshift_versions}")

    # Return the OpenShift versions as JSON
    if openshift_versions:
        return jsonify(openshift_versions)
    else:
        print("No OpenShift versions found")
        return jsonify(error='No OpenShift versions found'), 400

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Get OpenShift channel information.')
    parser.add_argument('--api', action='store_true', help='Start Flask app for OpenShift upgrades API')
    parser.add_argument('--version', help='The OpenShift version')
    parser.add_argument('--channel', help='stable, fast, candidate')

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.api:
        # Start the Flask app without threading
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        # Check if both --version and --channel are provided
        if not args.version and not args.channel:
            parser.error('Either --version or --channel must be provided.')

        # Use command-line arguments for channel and version
        openshift_versions = get_openshift_versions(args.channel, args.version)

        # Print the OpenShift versions
        for version in openshift_versions:
            print(version)