# Heb je Anaconda geïnstalleerd, dan zit de bagit-module daar al in.

import bagit
import os
from os.path import getsize, join, relpath, isdir

path = r"C:\path\to"

# Functies

def create_bag(path): # Functionaliteit toevoegen om een error te geven bij een lege map
    messageDigestAlgorithms = ['md5']
    bag_info = {'Contact-Name': 'Wim Lo', 
                'Source-Organization': 'Flanders Architecture Institute'}
    bag = bagit.make_bag(bag_dir = path, checksums = messageDigestAlgorithms, bag_info = bag_info)
    print(path, "bag created!")
    
def validate_bag(path, fast=None, completeness_only=None):
    bag = bagit.Bag(path) # Vooraleer je een path als bag kunt valideren moet je dit voor het systeem tot "bag" maken
    if fast == None and completeness_only == None:
        print(path, "bag validity:", bag.is_valid(fast=False, completeness_only=False)) # Deze functie geeft de waarde True of False terug.
    elif fast == True and completeness_only == None:
        print(path, "bag validity:", bag.is_valid(fast=True, completeness_only=False))
    else:
        print("Deze combo is fout of nog niet geprogrammeerd.")
              
def update_bag(path): # Een bag na wijziging nieuwe manifests geven
    bag = bagit.Bag(path)
    bag.save(manifests=True)
    
def bag_from_subfolders(path): # Maak bags van de subfolders in één specifieke folder aangegeven met path
    for direc in os.listdir(path):
        print("Working on:", direc)
        source_path = os.path.join(path, direc)
        if os.path.isdir(source_path):
            create_bag(source_path)
        
def validate_subfolders(path, fast=None, completeness_only=None): # Valideer subfolders als bags in één specifieke folder aangegeven met path
    for direc in os.listdir(path):
        print("Working on:", direc)
        source_path = os.path.join(path, direc)
        if os.path.isdir(source_path):
            validate_bag(source_path, fast, completeness_only)
              
def update_bag_from_subfolders(path): # bags in subdirectories nieuwe manifests geven
    for direc in os.listdir(path):
        print("Working on:", direc)
        source_path = os.path.join(path, direc)
        if os.path.isdir(source_path):
              update_bag(source_path)

# Subdirectories baggen
bag_from_subfolders(path)

# Een specifieke directory baggen
create_bag(path)

# Subdirectories valideren
validate_subfolders(path)

# Een specifieke directory valideren
validate_bag(path)

# Een bag updaten incl. wijziging van manifest (na deletion of addition van bestanden)
update_bag(path)

# Bags in subdirectories updaten incl. wijziging van manifest (na deletion of addition van bestanden)
update_bag_from_subfolders(path)
    
### DOCU (onderstaande tekst maakt geen deel uit van de code)
# Vanuit een Python-interpreter van de map "Gent_Tunnel" op mijn Desktop een bag maken.
# Contactnaam Wim Lo komt in de bag-info terecht.

# Goeie docu! onderaan deze pagina https://github.com/LibraryOfCongress/bagit-python

python -m bagit --contact-name 'WimLo' "c://Users//Wim Lo//Desktop//Gent_Tunnel"

python -m bagit --contact-name --md5 'WimLo' "c://Users//Wim Lo//Desktop//Gent_Tunnel" #Enkel md5

# Een volledige validatie.
python -m bagit --validate "c://Users//Wim Lo//Desktop//Gent_Tunnel"

# Een snelle validatie (geen checksums, maar wel structuur en bestandsgrootte)
python -m bagit --validate --fast "c://Users//Wim Lo//Desktop//Gent_Tunnel"

# ------------------
# Using BagIt from your Python code (dus in Jupyter basically)

import bagit


# Een bag maken en vervolgens de bag-informatie weergeven

path = r"windows\path\to"
messageDigestAlgorithms = ['md5']
bag_info = {'Contact-Name': 'Wim Lo', 
            'Source-Organization': 'Flanders Architecture Institute'}

bag = bagit.make_bag(bag_dir = path, checksums = messageDigestAlgorithms, bag_info = bag_info)

for x, y in bag.entries.items(): # De bag-informatie weergeven
    print(x, y['md5'])
    
# Een bag valideren

bag = bagit.Bag(path) # Vooraleer je een path als bag kunt valideren moet je dit voor het systeem tot "bag" maken
print(bag.is_valid(fast=False, completeness_only=False)) # Deze functie geeft de waarde True of False terug.
