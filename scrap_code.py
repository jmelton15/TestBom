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