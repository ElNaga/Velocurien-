import requests
import hashlib
import os
import logging

logger = logging.getLogger()

def download_json(url, folder_path, filename) -> bool:
    path_to_file = os.path.join(folder_path, filename)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    logger.info("Downloading " + url + " to " + path_to_file)
    response = requests.get(url)

    with open(path_to_file + ".tmp", "wb") as f:
        f.write(response.content)
        
    return check_hash_has_changed(path_to_file)

def check_hash_has_changed(path_to_file) -> bool:
    try:
        current_hash = open(path_to_file + ".md5").read()
    except FileNotFoundError:
        logger.info("No hash file found for " + path_to_file)
        current_hash = ""
    
    if os.path.exists(path_to_file):
        with open(path_to_file + ".tmp", "rb") as f:
            new_hash = hashlib.md5(f.read()).hexdigest()
        if current_hash == new_hash:
            logger.info("Hash has not changed for " + path_to_file + ". Keeping it.")
            os.remove(path_to_file + ".tmp")
            return False
        else:
            logger.info("Hash has changed for " + path_to_file + ". Replacing it.")
            os.remove(path_to_file)
            os.rename(path_to_file + ".tmp", path_to_file)
            open(path_to_file + ".md5", "w").write(new_hash)
    else:
        logger.info("No file found for " + path_to_file + ". Creating it.")
        os.rename(path_to_file + ".tmp", path_to_file)
        with open(path_to_file, "rb") as f:
            new_hash = hashlib.md5(f.read()).hexdigest()
        open(path_to_file + ".md5", "w").write(new_hash)
        
    return True
    