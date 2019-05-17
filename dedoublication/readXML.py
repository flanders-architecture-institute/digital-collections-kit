import xml.etree.ElementTree as ET # We gebruiken ElementTree. Zie voor handleiding: https://docs.python.org/3/library/xml.etree.elementtree.html
import pandas as pd
import re # Goed overzicht voor regular expressions: https://www.regular-expressions.info/refcharacters.html

xmlloc = "C:\\Users\\Wim Lo\\Desktop\\CK\\PREMIS_CK3.xml"
tree = ET.parse(xmlloc)

root = tree.getroot()
filelist = []
for file in root.findall('./{http://www.loc.gov/premis/v3}object'): 
    fileid = file.findtext('.//{http://www.loc.gov/premis/v3}objectIdentifierValue')
    filename = file.findtext('.//{http://www.loc.gov/premis/v3}originalName')
    contentlocation = file.findtext('.//{http://www.loc.gov/premis/v3}contentLocationValue')
    checksum = file.findtext('.//{http://www.loc.gov/premis/v3}messageDigest')
    foldersinpath = contentlocation.split('/') # Returns een lijst met de folders
    folder = foldersinpath[-2]
    filedict = {'foldername':folder, 'objectIdentifierValue':fileid, 'originalName':filename, 'contentLocationValue':contentlocation, 'messageDigest':checksum}
    filelist.append(filedict)
    
totallist = pd.DataFrame(filelist)
totallist.to_excel(xmlloc[:-3] + 'xlsx') # een xlsx met dezelfde naam wordt naast de xml geplaatst
