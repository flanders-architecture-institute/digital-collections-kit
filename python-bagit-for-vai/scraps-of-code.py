# Heb je Anaconda geïnstalleerd, dan zit de bagit-module daar al in.
# Vanuit een Python-interpreter van de map "Gent_Tunnel" op mijn Desktop een bag maken.
# Contactnaam Wim Lo komt in de bag-info terecht.

# Goeie docu! https://libraryofcongress.github.io/bagit-python/
# Nog beter: onderaan deze pagina https://github.com/LibraryOfCongress/bagit-python

python -m bagit --contact-name 'WimLo' "c://Users//Wim Lo//Desktop//Gent_Tunnel"

python -m bagit --contact-name --md5 'WimLo' "c://Users//Wim Lo//Desktop//Gent_Tunnel" #Enkel md5

# Een volledige validatie.
python -m bagit --validate "c://Users//Wim Lo//Desktop//Gent_Tunnel"

# Een snelle validatie (geen checksums, maar wel structuur en bestandsgrootte)
python -m bagit --validate --fast "c://Users//Wim Lo//Desktop//Gent_Tunnel"

# ------------------
# Using BagIt from your Python code (dus in Jupyter basically)
# Standaard sjabloon
import bagit
bag = bagit.make_bag('example-directory', {'Contact-Name': 'Ed Summers'})
print(bag.entries)

# Geteste code vanuit Jupyter: Veel zul je moeten achterhalen door de code van het programma: https://github.com/LibraryOfCongress/bagit-python/blob/master/bagit.py)
# Let hier dus goed op dat het checksumstatement in een lijst moet staan, ook al is het maar één item (de officiële docs op de Github rammelen hier zwaar)
import bagit
bag = bagit.make_bag(bag_dir = 'c://Users//Wim Lo//Documents//TMP//Set_adviesdocs', checksums = ['md5'], bag_info = {'Contact-Name': 'Wim Lo'})
print(bag.entries)
