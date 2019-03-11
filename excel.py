from Modules import Functions as f
from Modules import Variables as v
from Modules import Library_Class as c
import pandas as pd
import time

start = time.time()

# creating a dataframe out of the spreadsheet (default input and output excels)
spreadsheet = pd.read_excel(v.default_input_file)
input_writer = pd.ExcelWriter(v.default_input_file)
column_dict = {'filename': 'Library Name', 'hash': 'Sha 1', 'result': 'Result'}
#cleaning the input excel file
clean_spreadsheet = pd.DataFrame(data={column_dict[col]:[] for col in column_dict})
clean_spreadsheet.to_excel(input_writer, index=False)
input_writer.save()

# Creating lists out of the spreadsheet coulumns
filenames = list(spreadsheet[column_dict['filename']])
hashes = list((spreadsheet[column_dict['hash']]))
results = []

hash_results = {}
for file_hash_tuple in zip(filenames, hashes): # for each row in the excel file
    inst = c.Library(file_hash_tuple[0], str(file_hash_tuple[1])) # create a "Library" class instance
    message = "Suspected" 
    needed_versions = inst.get_needed_downloads()
    print(inst.pure_name + ': ', needed_versions)
    if not needed_versions: # if the package has no versions in Nuget
        message = "Package not found in Nuget"
        for package in hash_results:###############################
            if inst.sha_1.lower() in hash_results[package]:########
                message = "Match found in: " + package#############
        results.append(message)
        print(message)
        continue # to the next iteration (file,hash) tuple
    for version in needed_versions: 
        found_match_flag = False
        f.download_package(inst.pure_name, version)
        downloaded_package_name = inst.pure_name + '.' + version
        print("\n" + downloaded_package_name + '------ Downloaded. Hashes:')
        if not downloaded_package_name in hash_results:  
            if inst.is_package: # calculate the .nupkg files hash
                hash_results[downloaded_package_name] = [f.hash_calculator(v.default_path_to + downloaded_package_name + v.package_suffix)]
            else: # extract and calculate
                f.extract_package(downloaded_package_name + v.package_suffix)
                hash_results[downloaded_package_name] = f.hash_calculate_directory(downloaded_package_name) + [f.hash_calculator(v.default_path_to + downloaded_package_name + v.package_suffix)]
            print(hash_results[downloaded_package_name])
        for package in hash_results:
            if inst.sha_1.lower() in hash_results[package]:
                message = "Match found in: " + package
                found_match_flag = True
        if found_match_flag:
            print(message)
            break # to the next iteration (file,hash) tuple
        print(message)
    results.append(message)

print("Results:")
for result in results:
    print(result)

#saving the spreadsheet df to the default output excel file
output_writer = pd.ExcelWriter(v.default_output_file)
spreadsheet[column_dict['result']] = results
spreadsheet.to_excel(output_writer, index=False)
output_writer.save()


end = time.time()
print('\nExecution time:  ' + str(end - start))




    
    


