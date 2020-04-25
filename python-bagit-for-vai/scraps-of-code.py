# Heb je Anaconda geïnstalleerd, dan zit de bagit-module daar al in.
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

# Eén test: Een bag maken van de subdirectories

