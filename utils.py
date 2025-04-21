import os

def get_py_files(path):

    # print out os path file and directory 
    print(f"Is file? {os.path.isfile(path)}")
    print(f"Is dir? {os.path.isdir(path)}")


    py_files = []

    # check if file- ends with .py, ez pz
    if os.path.isfile(path) and path.endswith('.py'):
        py_files.append(path)

    elif os.path.isdir(path): # if folder
        # walking paths, appending full paths
        ### all subdirectories '_.'
        ### BFS type stuff
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    # grabs all paths, connecting to root
                    full_path = os.path.join(root, file)
                    # slaps em into py_files
                    py_files.append(full_path)
    
    else:
        # nyop
        print(f"Invalid path: {path}")

    return py_files