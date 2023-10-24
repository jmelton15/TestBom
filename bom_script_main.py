import subprocess
import os
import configparser
import utils

# First thing to do is to instantiate an object of the config.ini file
config = configparser.ConfigParser();
config.read('config.ini')

## Main method to run all the necessary functions in order
# Some of these functions are called from the imported utils.py file 
def main():
    #this function creates the temporary directories needed for the script and git cloning
    utils.setup_temp_dirs(config)

    run()


def run():
    repos = dict(config.items('Repos'))
    repos_directory = config.get("Temp_Dirs","repos_directory")
    bom_files = config.get("Temp_Dirs","bom_files_directory")
    for repo in repos:
        clone_repo(repos[repo])
        filename = f'{bom_files}sbom-{repo}.json'
        #we call this here to ensure that the necessary directories are created
        # in order to store the newly cloned git repos
        utils.create_directory(f"{repos_directory}{repo}")

        create_bom_file(filename)
        utils.custom_rmtree(f"{repos_directory}{repo}")
         

def clone_repo(repoLink):
    cmd = f'git clone {repoLink}'
    cmd_res = subprocess.call(cmd,shell=True)

def create_bom_file(filename):
    spec_version = config.get("CDXGEN","spec_version")
    cmd = f'cdxgen -o {os.getcwd()}/{filename} --spec-version {spec_version}'
    cmd_res = subprocess.call(cmd,shell=True)


if __name__ == '__main__':
    main()



#########
# This stuff below is for the server version of cdxgen
#########

# def create_sbom_from_repo(repoLink,file):
#     base_curl_url = config.get('Curl','base_curl_url')
#     cmd = f'curl -o {file} {base_curl_url}{repoLink}'
#     cmd_result = subprocess.call(cmd,shell=True)


# def run_sbom_creation():
#     time.sleep(10)
#     file_path = config.get("Curl","file_storage_path")
#     # Check if the directory already exists
#     create_directory(file_path)
#     repos = dict(config.items('Repos'))
#     for repo in repos:
#         file = f'{file_path}/{repo}_bom.json'
#         print("Creating Bom file for app: ", repo)
#         create_sbom_from_repo(repos[repo],file)
