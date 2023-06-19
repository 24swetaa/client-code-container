import requests
import argparse
import os
import random
from kubernetes import client, config
import logging
import datetime

BASE_URL = 'http://'

def get_pod_ip_and_port_by_name(pod_name):
    # Load the in-cluster Kubernetes configuration
    config.load_incluster_config()

    # Create the Kubernetes API client
    v1 = client.CoreV1Api()

    # Retrieve the pod information by name
    pod = v1.read_namespaced_pod(pod_name, 'default')
    pod_ip = pod.status.pod_ip

    # Retrieve the port number from the environment variable
    port_number = None
    for container in pod.spec.containers:
        if container.name == 'monitor':
            for env in container.env:
                if env.name == 'DOTNETMONITOR_Urls':
                    url = env.value
                    port_number = url.split(':')[-1]

    return pod_ip, port_number

# Configure logging to output to console with time and date
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

def trigger_monitor_action(action, pod_name, pid=None, uid=None, name=None,  duration=None, egressProvider=None, tags=None):
    pod_ip, port_number = get_pod_ip_and_port_by_name(pod_name)
    api_url = f"{BASE_URL.rstrip('/')}//{pod_ip}:{port_number}/{action.lstrip('/')}"
                 
    # Append pid as a query parameter if provided
    if pid is not None:
        api_url += f"?pid={pid}"

    # Append uid as a query parameter if provided
    if uid is not None:
        api_url += f"&uid={uid}"

    # Append name as a query parameter if provided
    if name is not None:
        api_url += f"&name={name}"

    # Append duration as a query parameter if provided
    if duration is not None:
        api_url += f"&duration={duration}"

    # Append egressProvider as a query parameter if provided
    if egressProvider is not None:
        api_url += f"&egressProvider={egressProvider}"

    # Append tags as a query parameter if provided
    if tags is not None:
        api_url += f"&tags={tags}"

    # Log the pod information
    logger.info(f"Pod Name: {pod_name}")
    logger.info(f"Pod IP Address: {pod_ip}")
    logger.info(f".NET Monitor URL Port: {port_number}")
    logger.info(f"Action: {action}")
    # Check if any parameters are provided
    if pid is None and uid is None and name is None and duration is None and egressProvider is None and tags is None:
        logging.info("No additional parameters provided.")
    else:
        if pid is not None:
            logging.info(f"pid: {pid}")
        if uid is not None:
            logging.info(f"uid: {uid}")
        if name is not None:
            logging.info(f"name: {name}")
        if duration is not None:
            logging.info(f"duration: {duration}")
        if egressProvider is not None:
            logging.info(f"egressProvider: {egressProvider}")
        if tags is not None:
            logging.info(f"tags: {tags}")
    logger.info(f"Generated URL: {api_url}")

    try:
        response = requests.get(api_url)
        logger.info("checking the response...")
        response.raise_for_status()
        logger.info(f"Response status: {response.status_code}")

        # # Generate a random number to append to the filename
        # random_number = random.randint(1, 100000)
        # logging.info(f"Random number generated: {random_number}")

        # # Save the response content to a text file with a random number appended to the filename
        # filename = f"response_{action.replace('/', '_')}_{random_number}.txt"
        # with open(filename, 'w', encoding='utf-8') as file:
        #     file.write(response.text)
        # # print(f"Response saved to file: {filename}")
        # logging.info(f"Response saved to file: {filename}")
        # Save the response content to the specified output file

        # Save the response content to a file
        with open('/app/response/response.txt', 'w', encoding='utf-8') as file:
            file.write(response.text)

        logger.info(f"Response saved to file: /app/response/response.txt")
        logger.info(f"Response status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logger.error(f'RequestException error occurred: {str(e)}')

def main():

    parser = argparse.ArgumentParser(description='Trigger .NET Monitor actions.')
    parser.add_argument('--action', required=True, help='Action to perform in the .NET Monitor')
    parser.add_argument('--pod-name', required=True, help='Name of the pod')
    parser.add_argument('--pid', help='Process ID')
    parser.add_argument('--uid', help='UID')
    parser.add_argument('--name', help='Name')
    parser.add_argument('--duration', help='Duration')
    parser.add_argument('--egressProvider', help='Egress Provider')
    parser.add_argument('--tags', help='Tags')

    args = parser.parse_args()

    pid=None
    uid=None
    name=None
    duration=None
    egressProvider=None
    tags=None

    if args.pid != "NO_PID":
        pid=args.pid
    if args.uid != "NO_UID":
        uid=args.uid
    if args.name != "NO_NAME":
        name=args.name
    if args.duration != "NO_DURATION":
        duration=args.duration
    if args.egressProvider != "NO_EGRESS_PROVIDER":
        egressProvider=args.egressProvider
    if args.tags != "NO_TAG":
        tags=args.tags


    trigger_monitor_action(
        args.action,
        args.pod_name,
        pid=pid,
        duration=duration,
        uid=uid,
        name=name,
        egressProvider=egressProvider,
        tags=tags
    )

if __name__ == '__main__':
    main()
