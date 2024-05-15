import numpy as np
import os
import PIL.Image


def SaveImage(image:np.ndarray, filename:str):
    if '/' in filename or '\\' in filename:
        idx_slash = filename[::-1].find('/')
        idx_islash = filename[::-1].find('\\')
        # The last thing is '/'
        if idx_islash == -1 or 0 <= idx_slash < idx_islash: 
            idx = idx_slash - len(filename)
        # The last thing is '\\'
        else:
            idx = idx_islash - len(filename)

        directory = filename[:-idx]
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    im = PIL.Image.fromarray(image)
    im.save(filename)