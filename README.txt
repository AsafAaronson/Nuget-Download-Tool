===========
INSTALLATION:
Download Python 3.7 or higher from https://www.python.org/
(When installing make sure it sets python to "PATH" by default so that pip can be used to install packages)
Install pipenv (using pip)
Run the following command in the CMD from the “Nuget Download Tool” Directory: “pipenv install”. This will install all dependencies used by this project.
Once the dependencies have been installed you are good to go!

===========
HOW TO USE:

1) Excel Mode: 
Fill a list of libraries and their sha1 hashes to the “Input.xlsx” excel file.
Run the following command in the CMD from the “Nuget Download Tool” Directory: “pipenv run excel.py”.
When the script finishes running, the results will be shown in the “Output.xlsx” Excel.

The result for each library will be one of three options:
-Package was not found-  If the package wasn’t found on Nuget in this exact name.

-Suspected - If the package is found but had no Sha1 match in any of the versions.

-Match Found in: <package name.version> - If the hash matched one of the hashes in the package in the version.

2) On Demand Mode
Insert a package name, a version(optional) and a suffix(optional).
Examples: project-1.1.8.nupkg  -  project.2.2.0.dll  -  project-1.3.2.exe  -  project

According to the parameters given, the script will download the package 
in the requested version, or in all existing versions if no valid version is given.
Then it will print out all the hashes of the package files inside as well as the hash of the package itself.

Once in a while you should clean out the "package downloads" folder which contains all the downloaded data.

===========
HOW IT WORKS:

The scripts for both modes use a set of outer "modules".
These are functions, default parameters and a class that are written seperately from the scripts and are located in Modules directory.
-Library_Class- is a class that accepts a raw library name and sha 1. Then manipulates the raw name into a package name, version and whether it's a package or file.
-Functions - is a set of functions used in the scripts.
-Variables -  is a set of default parameters used in the scripts and can be changed.

Excel Mode:
The excel mode accepts the data from the default input excel file (You can set a different input file in the Variables module)
For each row (library and hash) the script downloads the relevant versions (decided in the Library Class module) from newest to oldest.
For each downloaded version it extracts the package and all the files contained in them and calculates the hashes for the file inside (.dll and .exe- this can be configured in the variables module)
The given hash  is then matched to the calculated ones so that if a match is found it stops downloading the package versioons and moves on to the next excel row.
The relevant result is assigned to the row according to the outcome of the matching proccess.
After assigning results for all the rows in the excel file it will print the results to the CMD console and print them to the default output excel file (This can be configured in the Variables module)

