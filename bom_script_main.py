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
    # #this function clones repos from the list of repos in the config.ini file
    # clone_multiple_repos()
    # #this function creates all the bom.json files from the cloned repos and names them accordingly
    # create_multiple_bom_files()

    # upload_all_bom_files()

    # #this function can be used to remove all the temporarily created directories and files
    # # just_repos (second parameter) is defaulted to True to delete only the cloned repos after the Bom files are created
    # utils.cleanup_files(config,True)
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


###
# This function clones a singule git repo by calling a windows command using subprocess library
#  It takes in two params:
# Param 1: repoLink (string) => link to the git repo
# Param 2: savePath (string) => path where you'd like to save the repo to when cloned
###
def clone_repo_withpath(repoLink, savePath):
    cmd = f'git -C {savePath} clone {repoLink}'
    cmd_res = subprocess.call(cmd,shell=True)

###
# This function loops over a list of repos in the config.ini file and clones repos using the
#  clone_repo() function above
###
def clone_multiple_repos():
    repos = dict(config.items('Repos'))
    for repo in repos:
        repos_directory = config.get("Temp_Dirs","repos_directory")

        #we call this here to ensure that the necessary directories are created
        # in order to store the newly cloned git repos
        utils.create_directory(f"{repos_directory}{repo}")

        save_path = f"{repos_directory}{repo}"
        clone_repo(repos[repo],save_path)

###
# This function creates a singular bom.json file from a given directory using a windows command
# with the subprocess library.
#  It takes in two params:
# Param 1: dirPath (string) => path to the directory where you'd like to call the command in
# Param 2: fileToCreate (string) => path/name of the bom file you'd like to create
###
def create_bom_from_dir(dirPath,fileToCreate):
    spec_version = config.get("CDXGEN","spec_version")
    cmd1 = f'cdxgen -o {os.getcwd()}/{fileToCreate} --spec-version {spec_version}'
    cmd1_res = subprocess.call(cmd1,cwd=dirPath,shell=True)

###
# This function loops over a list of directories in the config.ini file and creates many bom.json
# files using the create_bom_from_dir() function above
###
def create_multiple_bom_files():
    file_path = config.get("Temp_Dirs","bom_files_directory")
    repos_directory = config.get("Temp_Dirs","repos_directory")
    try:
        directories = os.listdir(repos_directory)
        folders = [folder for folder in directories if os.path.isdir(os.path.join(repos_directory, folder))]
        for folder in folders:
            file = f'{file_path}{folder}_bom.json'
            create_bom_from_dir(f'{repos_directory}{folder}',file)
    except FileNotFoundError:
        print(f'Directory {repos_directory} not found')
    except Exception as e:
        print(f"Error traversing directory {repos_directory}: {e}")
    # dirs = dict(config.items('Temp_Dirs'))
    # for repo in dirs:
    #     file = f'
    #     create_bom_from_dir(dirs[repo],file)


def upload_all_bom_files():
    bom_files = config.get("Temp_Dirs","bom_files_directory")
    try:
        for root, dirs, files in os.walk(bom_files, topdown=False):
            for name in files:
                print(name)
    except FileNotFoundError:
        print(f'Directory {bom_files} not found')
    except Exception as e:
        print(f"Error traversing directory {bom_files}: {e}")



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
