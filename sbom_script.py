import subprocess
import os
import configparser


config = configparser.ConfigParser();
config.read('config.ini')


def create_sbom_from_repo(repoLink,file):
    base_curl_url = config.get('Curl','base_curl_url')
    cmd = f'curl -o {file} {base_curl_url}{repoLink}'
    cmd_result = subprocess.call(cmd,shell=True)


def run_sbom_creation():
    file_path = config.get("Curl","file_storage_path")
    # Check if the directory already exists
    create_directory(file_path)
    repos = dict(config.items('Repos'))
    for repo in repos:
        file = f'{file_path}/{repo}_bom.json'
        print("Creating Bom file for app: ", repo)
        create_sbom_from_repo(repos[repo],file)


def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # If not, create the directory
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")


run_sbom_creation()

