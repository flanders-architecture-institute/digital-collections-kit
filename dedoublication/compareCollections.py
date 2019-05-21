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

resdf = pd.merge(subjectdf, testcorp, on='messageDigest', how='left') # Er wordt een join gecreëerd - dit kan bij grote excels erg groot worden!!
resdf['doubleCount'] = resdf.groupby('contentLocationValue')['contentLocationValue'].transform('count') # Dit geeft een gigaframe met per bestand het de bestanden uit testcorp waarvoor er een match bestaat. Dit naar een Excel brengen duurt erg lang.
resdf = resdf.groupby(['contentLocationValue', 'objectIdentifierValue', 'originalName', 'messageDigest', 'doubleCount'])['filename'].agg('count').reset_index()
resdf = resdf.drop(columns=['filename']) # Ziet er allemaal niet proper gecodeerd uit, maar het werkt

# Stap 3: We maken een kolom 'uniek', 'nietUniek'
def uniek(cellValue):
    if cellValue > 1:
        return "notUnique"
    else:
        return "Unique"

resdf['uniqueOnDisk'] = resdf['doubleCount'].apply(uniek)

# Stap 4: We creëren een extra kolom met de folders die voorwerp zijn van onderzoek (één niveau onder researchloc)

def folder(cellValue):
    cellValue = re.sub('^' + researchloc + '/', '', cellValue)
    cellValue = cellValue.split('/')[0] # We splitsen het resterende path op en nemen de eerste waarde van de resulterende lijst
    return cellValue

resdf['researchedFolder'] = resdf['contentLocationValue'].apply(folder)
resdf
