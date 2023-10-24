import os
import stat


def parse_repo_link(repoLink):
    splitLink = repoLink.split('/')
    return splitLink[len(splitLink)-1]

def create_directory(directory_path):
    # Check if the directory already exists
    if not os.path.exists(directory_path):
        # If not, create the directory
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

def setup_temp_dirs(config):
    temp_dirs = dict(config.items('Temp_Dirs'))
    for directory in temp_dirs:
        create_directory(temp_dirs[directory])

def custom_rmtree(starting_dir):
    for root, dirs, files in os.walk(starting_dir, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(starting_dir)      


def cleanup_files(config,just_repos):
    if just_repos:
        directory = config.get("Temp_Dirs","repos_directory")
        try:
            print("Cleaning Up Cloned Repos...")
            custom_rmtree(directory)
        except FileNotFoundError:
            print(f"Directory {directory} not found!")
        except Exception as e:
            print(f"Error removing directorie(s): {e}")
    else:
        dirs = dict(config.items('Temp_Dirs'))
        for directory in dirs:
            try:
                print("Cleaning Up Temp Directories and Files...")
                custom_rmtree(dirs[directory])
            except FileNotFoundError:
                print(f"Directory {directory} not found!")
            except Exception as e:
                print(f"Error removing directorie(s): {e}")
    