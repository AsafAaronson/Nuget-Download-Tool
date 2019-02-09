from Modules import Functions as f
from Modules import Variables as v
from Modules import Library_Class as c
import pandas as pd
import time

def on_demand_process():
    input_data = input("\n\n" + "="*20 + "\nThe On Demand Mode:\nType the name of the project, the version (if you have one) and if it's a Nuget Package or a dll/exe\nIf the package \
in the version exists it will be downloaded, if no version is given all versions will be downloaded\nExamples: \
project-1.1.8.nupkg  -  project.2.2.0.dll  -  project-1.3.2.exe  -  project\nInput:\n")

    start = time.time()
    inst = c.Library(input_data,"No Hash")
    needed_versions = inst.get_needed_downloads()
    if not needed_versions:
        print("This Package has no versions in Nuget")
    else:
        print(inst.clean_package_name, needed_versions)
        for version in needed_versions:
            f.download_package(inst.pure_name,version)
            downloaded_package_name = inst.pure_name + '.' + version
            if inst.is_package: # calculate the .nupkg files hash
                print(downloaded_package_name, f.hash_calculator(v.default_path_to + downloaded_package_name + v.package_suffix)) 
            else: # extract and calculate + the .nupkg hash
                f.extract_package(downloaded_package_name + v.package_suffix)
                print (downloaded_package_name, f.hash_calculate_directory(downloaded_package_name), "Package Hash-" + f.hash_calculator(v.default_path_to + downloaded_package_name + v.package_suffix))

    end = time.time()
    print('\nExecution time:  ' + str(end - start))
    on_demand_process()

on_demand_process()
