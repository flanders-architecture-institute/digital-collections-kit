# Heb je Anaconda geïnstalleerd, dan zit de bagit-module daar al in.
# Vanuit een Python-interpreter van de map "Gent_Tunnel" op mijn Desktop een bag maken.
# Contactnaam Wim Lo komt in de bag-info terecht.
python -m bagit --contact-name 'WimLo' "c://Users//Wim Lo//Desktop//Gent_Tunnel"

python -m bagit --contact-name --md5 'WimLo' "c://Users//Wim Lo//Desktop//Gent_Tunnel" #Enkel md5

# Een volledige validatie.
python -m bagit --validate "c://Users//Wim Lo//Desktop//Gent_Tunnel"

# Een snelle validatie (geen checksums, maar wel structuur en bestandsgrootte)
python -m bagit --validate --fast "c://Users//Wim Lo//Desktop//Gent_Tunnel"


# Using BagIt from your Python code:

    import bagit
    bag = bagit.make_bag('example-directory', {'Contact-Name': 'Ed Summers'})
    print(bag.entries)
