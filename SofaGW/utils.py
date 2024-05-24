import os
import numpy as np
import PIL.Image

# >>> Related file/folder/directory >>>

def mkdir(filename: str):
    """make directory 
    filename can include a file e.g. dir/file.py.
    """
    if '/' in filename or '\\' in filename:
        idx_slash = filename[::-1].find('/')
        idx_islash = filename[::-1].find('\\')
        # The last thing is '/'
        if idx_islash == -1 or 0 <= idx_slash < idx_islash: 
            idx = idx_slash - len(filename) + 1
        # The last thing is '\\'
        else:
            idx = idx_islash - len(filename) + 1

        directory = filename[:-idx]
        if not os.path.exists(directory):
            os.makedirs(directory)

def clear_folder(directory):
    """
    input param
        directory : (str) directory to clear. e.g. dir1/dir2 not dir1/dir2/
    """
    directory
    import os, glob

    # Loop over all files and delete them one by one
    for file in glob.glob(directory+"/*"):
        os.remove(file)
        print("Deleted " + str(file))

def upper_directory(filename, step=0) -> str:
    """ex. when step=0,
    directory/filename.exe -> directory
    dir1/dir2/ -> dir1/dir2
    dir1/dir2 -> dir1
    <SofaGuidewireNav>/SofaGW/utils.py -> <SofaGuidewireNav>/SofaGW
    """
    directory = os.path.dirname(filename)
    for i in range(step):
        directory = os.path.dirname(directory)
    return directory

root_dir = upper_directory(os.path.abspath(__file__), 1)


def SaveImage(image:np.ndarray, filename:str):
    mkdir(filename=filename)

    im = PIL.Image.fromarray(image)
    im.save(filename)

# <<< Related file/folder/directory <<<

if __name__ == "__main__":
    print(root_dir)
    print(os.path.abspath(__file__))
    print(upper_directory('<SofaGuidewireNav>/SofaGW/utils.py'))