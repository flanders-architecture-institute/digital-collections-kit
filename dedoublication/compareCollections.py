import pandas as pd
import re

# Onderstaande code checkt op basis van checksums hoe vaak de bestanden in subjectdf voorkomen in testcorp en geeft statistieken per subfolder in een gekozen folder
# Deze code gaat uit van een subjectdataframe dat resulteert uit het inlezen van een PREMIS-XML volgens onderzoek van Henk Vanstappen uit 2017.

subjectdf = pd.DataFrame('the content resource') # Kan komen uit een Json, een Premis-XML (zie hiervoor code), een Excel etc.
testcorp = pd.read_excel('the content resource') # Kan komen uit een Json, een Premis-XML (zie hiervoor code), een Excel etc.

# Stap 1: De gebruiker geeft aan in welke locatie hij de folders wilt onderzoeken

researchloc = input('Welke xlink wil je onderzoeken? ') 
subjectdf = subjectdf[subjectdf['contentLocationValue'].str.match(researchloc)] # str.match zoekt alle strings die starten met een gegeven string

# Stap 2: We zoeken hoe vaak een bestand uit de subjectdf voorkomt in het testcorp (a.h.v. MD5-checksum)

testcorp['doubleCount'] = testcorp.groupby('messageDigest')['messageDigest'].transform('count')
testcorp = testcorp.groupby(['messageDigest', 'doubleCount'])['filename'].agg('count').reset_index()
testcorp = testcorp.drop(columns=['filename'])
resdf = pd.merge(subjectdf, testcorp, on='messageDigest', how='left') # Er wordt een join gecreëerd - dit kan bij grote excels erg groot worden!!

# Stap 3: We maken een kolom om de status van de dubbel aan te geven.

def uniek(cellValue):
    if cellValue > 14:
            return "probSystemFile"
        elif cellValue > 4:
            return "manyDupes"
        elif cellValue > 1:
            return "someDupes"
        else:
            return "unique"

resdf['uniqueOnDisk'] = resdf['doubleCount'].apply(uniek)

# Stap 4: We creëren een extra kolom met de folders die voorwerp zijn van onderzoek (één niveau onder researchloc)

def folder(cellValue):
    cellValue = re.sub('^' + researchloc + '/', '', cellValue)
    cellValue = cellValue.split('/')[0] # We splitsen het resterende path op en nemen de eerste waarde van de resulterende lijst
    return cellValue

resdf['researchedFolder'] = resdf['contentLocationValue'].apply(folder)
resdf['filesInFolder'] = resdf.groupby('researchedFolder')['researchedFolder'].transform('count')

# Stap 5: We doen enkele berekeningen van het aantal occurrences van specifieke dubbelen
resdf['uniquesInFolder'] = resdf.loc[resdf['uniqueOnDisk'] == 'unique'].groupby('researchedFolder')['uniqueOnDisk'].transform('count')
resdf['someDupesInFolder'] = resdf.loc[resdf['uniqueOnDisk'] == 'someDupes'].groupby('researchedFolder')['uniqueOnDisk'].transform('count')
resdf['manyDupesInFolder'] = resdf.loc[resdf['uniqueOnDisk'] == 'manyDupes'].groupby('researchedFolder')['uniqueOnDisk'].transform('count')
resdf['probSystemFileInFolder'] = resdf.loc[resdf['uniqueOnDisk'] == 'probSystemFile'].groupby('researchedFolder')['uniqueOnDisk'].transform('count')

# Stap 6: We creëren een dataframe met rij per folder. Op die manier krijgen we een helder overzicht.
folderdf = resdf.drop(columns=['contentLocationValue', 'objectIdentifierValue', 'originalName', 'messageDigest', 'doubleCount', 'uniqueOnDisk'])
folderdf = folderdf.groupby('researchedFolder')['filesInFolder', 'uniquesInFolder', 'someDupesInFolder', 'manyDupesInFolder', 'probSystemFileInFolder'].agg('mean').reset_index()
folderdf 
