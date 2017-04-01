import requests
from tqdm import tqdm
from requests.utils import unquote
import os


def download_file(url,filename=None,chunk_size=512, directory=os.getcwd(), auth=None, total_size=None):

    #if no filename is given, try and get it from the url
    if not filename: 
        filename = unquote(url.split('/')[-1])
        
    full_name = os.path.join(directory,filename)
    
    #make the destination directory, but guard against race condition
    if not os.path.exists(os.path.dirname(full_name)):
        try:
            os.makedirs(os.path.dirname(full_name))
        except OSError as exc: 
            raise Exception('something failed')

    r = requests.get(url, stream=True, auth=auth)
    
    total_size = float(r.headers.get('Content-Length',total_size))
    n_iter = int(total_size/chunk_size)+1 

    with open(full_name, 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=n_iter) : 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    r.close()
