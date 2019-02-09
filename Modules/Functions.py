# A module used to organize raw library names into the pure name (the string without the suffix if it had one) and version if it had one
import requests, zipfile, os, hashlib, time
import pandas as pd
from pandas import ExcelWriter
from Modules import Variables as v



#accepts a string and a list of suffixes. returns the pure name
def shave_suffix(string, suff_list):
    try:
        for suff in suff_list:
            if string.endswith(suff):
                return string[:string.find(suff):]
    except AttributeError:
        pass
    return string
    
# accepts a string. returns a list:
# [pure name, version (any substring that has '.' or '-' followed by a number)]
def split_version(string):
    for i in range(len(string)):
        if string[i] == '-' or string[i] == '.':
            try:
                float(string[i + 1])
                return [string[:i:], string[i + 1::]]
                break
            except ValueError:
                pass
    return [string, ""]

# accepts a string and a list of suffixes. returns a list:
# [pure name, version (or "" if has no version)]
def clean_name(string, suff_list):
    return split_version(shave_suffix(string, suff_list))


# accepts the pure name of a package and a version. downloads the given package in the given version. returns None
def download_package(pure_name, version):
    down_link = requests.get(
        '%s%s/%s/%s.%s%s' % (v.ENDPOINT, pure_name , version, pure_name , version, v.package_suffix),
        allow_redirects=True)
    if down_link.status_code == requests.codes.ok:
        pure_file_path = '%s%s.%s' % (v.default_path_to, pure_name, version)
        file_path = pure_file_path + v.package_suffix 
        if not os.path.isfile(file_path):  # if the package with the same name doesn't exist
            with open(file_path, 'wb') as new_file: # saves the file as "library.version.nupkg"
                new_file.write(down_link.content)


# accepts a name of a directory to be made and creates it. if it already exists, recursively adds (copy)
# -----is called in extract_package-----
def create_directory(directory_name):
    try:
        os.makedirs(v.default_path_to + directory_name)
        return directory_name
    except FileExistsError:
        return create_directory(directory_name + '(copy)')


# accepts the full name of the file to unzip and the directory to unzip to. returns None. -----is called in extract_package-----
def unzip(file_name, directory_name):
    with zipfile.ZipFile(v.default_path_to + file_name, 'r') as zip_ref:
        zip_ref.extractall(v.default_path_to + directory_name)


# accepts the full name of the package to extract. creates a directory with it's pure name. unzips to that directory
def extract_package(file_name):
    pure_name = shave_suffix(file_name, v.list_of_suffixes)
    created_dir = create_directory(pure_name)
    unzip(file_name, created_dir)


# accepts a path to a file. calculates the files sha 1 hash. returns the hash. ------is called in hash_calculate directory----
def hash_calculator(path):
    with open(path, 'rb') as file:
        file_content = file.read()
        hasher = hashlib.sha1()
        hasher.update(file_content)
        final_hash = hasher.hexdigest()
    return final_hash.lower()


# accepts an existing directory name. calculates the hash for each file that ends with the suffix  in it,
# runs itself on every directory in it.returns a list of all the hashes calculated
def hash_calculate_directory(directory_name):
    hashes = []
    path = v.default_path_to + '/' + directory_name
    for filename in os.listdir(path):
        path_filename = path + '/' + filename
        if os.path.isdir(path_filename):
            hashes += hash_calculate_directory(directory_name + '/' + filename)
        else:
            for suff in v.list_of_suffixes:
                if filename.endswith(suff):
                    hashes.append(hash_calculator(path_filename))
    return hashes
    
