import os

path = r"path\to" # Gebruik de "r" en dan de string met backslashes voor Windowspaths. Je kunt ook gewone slashes gebruiken.

os.chdir(path) # os is nu de directory
os.getcwd() # Hiermee controleer je nog eens of je in de juiste directory zit te werken
os.chdir("..") # Ik ga naar de bovenliggende directory
os.chdir("to" # Ik ga naar een onderliggend relative path
print(os.path.dirname(path)) # Ik geef de bovenliggende directory weer
os.listdir(path) # Wat zit er eigenlijk in dit directory 

# De "walk" functie. Hiermee creëren we onze tree. Je kunt kiezen topdown of niet te werken.
# Per folder ontstaat een object met "de naam van de folder", "de naam van subfolders", "de naam van files"
# Het geeft een object terug van het type 'generator', dat moet worden geloopt

# Onderstaande code geeft per folder in de tree het aantal bytes en het aantal files per folder. Het genereert ook een lijst van lege folders die kunnen worden gedeleted.

deleted_dirs = []
for root, dirs, files in os.walk(path2):
    print(root, "| aantal bytes: ", end=" ")
    print(sum(getsize(join(root, name)) for name in files), "| aantal bestanden:", end =" ") # per bestandsnaam (name) in de lijst (files) wordt de size berekend en opgeteld
    print(len(files))
    if len(files) == 0 and len(dirs) == 0:
        deleted_dirs.append(root)
    
print()
print("directories to delete:")
for deldir in deleted_dirs:
    print(deldir)
