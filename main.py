import requests
import argparse

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

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Get OpenShift upgrade information.')
    parser.add_argument('--channel', required=True, choices=['fast', 'stable', 'candidate'], help='The upgrade channel')
    parser.add_argument('--version', required=True, choices=['4.14', '4.12', '4.10'], help='The OpenShift version')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    openshift_versions = get_openshift_versions(args.channel, args.version)

    # Print the OpenShift versions
    for version in openshift_versions:
        print(version)