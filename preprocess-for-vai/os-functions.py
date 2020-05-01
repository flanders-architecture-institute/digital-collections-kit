import os
import math # we use it for calculations for human readable file size
from datetime import datetime # we use it to transform dates in seconds to yyyy-mm-dd format
from os.path import getsize, join, relpath, isdir, isfile

# https://github.com/tw4l/brunnhilde/blob/master/brunnhilde.py: Zeer veel nuttige voorbeelden voor os commands vinden we in de brunnhilde code

path = r"path\to" # Gebruik de "r" en dan de string met backslashes voor Windowspaths. Je kunt ook gewone slashes gebruiken.

def convert_size(size):
    # convert size to human-readable form, stolen from Tim Walshe's Brunnhilde
    if (size == 0):
        return '0 bytes'
    size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p)
    s = str(s)
    s = s.replace('.0', '')
    return '%s %s' % (s,size_name[i])

#basics van os

os.chdir(path) # os is nu de directory
os.getcwd() # Hiermee controleer je nog eens of je in de juiste directory zit te werken
os.chdir("..") # Ik ga naar de bovenliggende directory
os.chdir("to" # Ik ga naar een onderliggend relative path
print(os.path.dirname(path)) # Ik geef de bovenliggende directory weer
os.listdir(path) # Wat zit er eigenlijk in dit directory 

# Overzicht van contents van een map, zonder subdirs. Gebruik if statement in combo met isfile of isdir

for item in os.listdir(path):
    if os.path.isfile(os.path.join(path, item)):
        print(item)
         
# Overzicht van een de contents van een directory met file-attributes

print("Files and Directories in '% s':" % path)
for item in os.scandir(path): #scandir geeft een dirEntry object terug met info per item in het path, waarover je moet loopen. Info over dirEntry: https://docs.python.org/3/library/os.html#os.DirEntry
    name = item.name
    result_path = item.path
    info = item.stat() # Met stat() spreek je een klasse aan die in een scandir klasse zit.
    print(name)
    if item.is_file():
        print("file")
    if item.is_dir():
        print("directory")
    if item.is_symlink():
        print("symlink")
    print("has path: ", result_path)
    print("has machine size: ", info.st_size)
    print("has human readable size: ", convert_size(info.st_size))
    print("last modified time: ", info.st_mtime)
    print("last modified time, human readable: ", datetime.fromtimestamp(info.st_mtime))
    print("creation on Windows or most recent metadata change on Unix: ", info.st_ctime)
    print("creation on Windows, or most recent metadata change on Unix, human readable: ", datetime.fromtimestamp(info.st_ctime))
    print()
         
# De "walk" functie. Hiermee creëren we onze tree. Je kunt kiezen topdown of niet te werken.
# Per folder ontstaat een object met "de naam van de folder", "de naam van subfolders", "de naam van files"
# Het geeft een object terug van het type 'generator', dat moet worden geloopt

# Opnieuw een functie: een overzicht van de inhoud van een folder, maar dan ook MET subdirs
# Er zijn verschillende mogelijkheden om dit te realiseren, maar wij doen steeds een scandir van de root.
# Dit lijkt ons efficiënter dan steeds opnieuw per file een stat te geven.

print("Tree of Files and Directories in '% s':" % path)
for root, dirs, files in os.walk(path): # os.walk() geeft een overzicht terug van files en folders in iedere folder
    for item in os.scandir(root):
        name = item.name
        result_path = item.path
        info = item.stat() # Met stat() spreek je een klasse aan die in een scandir klasse zit.
        print(name)
        if item.is_file():
            print("file")
        if item.is_dir():
            print("directory")
        if item.is_symlink():
            print("symlink")
        print("has path: ", result_path)
        print("has machine size: ", info.st_size)
        print("has human readable size: ", convert_size(info.st_size))
        print("last modified time: ", info.st_mtime)
        print("last modified time, human readable: ", datetime.fromtimestamp(info.st_mtime))
        print("creation on Windows or most recent metadata change on Unix: ", info.st_ctime)
        print("creation on Windows, or most recent metadata change on Unix, human readable: ", datetime.fromtimestamp(info.st_ctime))
        print()
         
         
# Onderstaande code geeft per folder in de tree het aantal bytes en het aantal files per folder. Het genereert ook een lijst van lege folders die kunnen worden gedeleted.

dirs_to_delete = []
for root, dirs, files in os.walk(path):
    print(root, "| aantal bytes: ", end=" ")
    print(sum(getsize(join(root, name)) for name in files), "| aantal bestanden:", end =" ") # per bestandsnaam (name) in de lijst (files) wordt de size berekend en opgeteld
    print(len(files))
    if len(files) == 0 and len(dirs) == 0:  # m.a.w. als er 100 % zeker niets in de folder zit...
        dirs_to_delete.append(root) # ... Lijst de folder dan op in een lijst genaamd dirs_to_delete
    
print()
print("directories to delete:")
for deldir in dirs_to_delete:
    print(deldir) # Controleer eerst of de lijst met dirs to delete klopt
         
#!! Noteer onderstaand codeblokje voor de zekerheid in een aparte Jupytercel
for deldir in dirs_to_delete: # Onderstaande code delete vervolgens lege folders op basis van de lijst. (Kan ook in bovenstaande code worden verwerkt, maar de lijst eerst checken is veiliger.
         os.rmdir(deldir)
         print(deldir, "deleted")
         
# Deze code maakt van een mappenstructuur van bestanden een platte lijst van bestanden.
# De ordening wordt behouden door het path op te nemen in de naam.
# folders worden in de bestandsnaam hier (in testmodus) gescheiden door een koppelteken. Aan te raden valt om in productie eerst de filename te wijzigen door alle underscores te vervangen in koppeltekens (Controleer) en vervolgens een underscore te nemen ter aanduiding van een folder.

os.chdir(path) # Nodig om vlot te kunnen renamen (= verplaatsen)
for root, dirs, files in os.walk(path):
    for name in files:
        tempsource = join(root,name) # ieder file krijgt zijn absoluut path door root en filename te combineren.
        source = os.path.relpath(tempsource, start=path) # Wij willen enkel een relatief path in de bestandsnaam steken. Via deze code krijg je een relatief path t.o.v. de variabele "path". Dit kunnen we verwerken in een nieuwe bestandsnaam...
        destination = path + "\\" + source.replace("\\", "-") # ... Door simpel een backslash te vervangen door een koppelteken.
        os.rename(source, destination)
