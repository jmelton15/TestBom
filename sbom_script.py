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


# def run_test():
#     cmd1 = f'cdxgen --server'
#     cmd2 = f'curl -o bom.json http://127.0.0.1:9090/sbom?url=https://github.com/jmelton15/TestJenkinsBom.git'
#     # cmd1_res = subprocess.call(cmd1,shell=True)
#     # cmd2_res = subprocess.call(cmd2,shell=True)

#     final_cmd = f'{cmd1} & {cmd2}'
#     res = subprocess.call(final_cmd,shell=False)



# run_test()

