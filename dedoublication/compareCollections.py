subjectdf = pd.DataFrame('the content resource')
testcorp = pd.read_excel('the content resource')

# Onderstaande code checkt op basis van checksums hoe vaak de bestanden in subjectdf voorkomen in testcorp.

newdf = pd.merge(subjectdf, testcorp, on='messageDigest', how='left') # Er wordt een join gecreëerd - dit kan bij grote excels erg groot worden!!
doubledf = newdf.dropna() # Dit geeft een gigaframe met per bestand het de bestanden uit testcorp waarvoor er een match bestaat. Dit naar een Excel brengen duurt erg lang.
resultdf = doubledf['contentLocationValue'].value_counts() # Een nieuw datframe wordt gemaakt met per folderpath het aantal keer dat het voorkomt.
resultdf.to_excel('C:\\Users\\Wim Lo\\Desktop\\CK\\resultdf.xlsx')
