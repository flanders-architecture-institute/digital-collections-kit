import os
import math # we use it for calculations for human readable file size
from datetime import datetime # we use it to transform dates in seconds to yyyy-mm-dd format
from os.path import getsize, join, relpath, isdir, isfile
import json
import time
import pandas as pd

def convert_size(size): # convert size to human-readable form, stolen from Tim Walshe's Brunnhilde
    if (size == 0):
        return '0 bytes'
    size_name = ("bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p)
    s = str(s)
    s = s.replace('.0', '')
    return '%s %s' % (s,size_name[i])

def filelist_nonrecursive(path):
# Maakt een simpele lijst van alle files en folders. Gebruik de analyze functies om meer gegevens te verkrijgen per item
    
    filelist = os.listdir(path)
    return filelist

def analyze_nonrecursive(path, files = True, dirs = True, symlink = True, printtype = True):
# Deze functie creëert een overzicht van alle files, folders en symlinks in een bepaalde folder. 
# We gaan hier ook uit van meteen printen voor weergave

    results = {'pathScanned': str(path)}
    itemlist = []
    for item in os.scandir(path): # Scandir is de niet-recursieve walk
        itemdict = {}
        if symlink == False:
            if item.islink():
                continue
        if files == False:
            if item.isfile():
                continue
        if dirs == False:
            if item.isdir():
                continue
        info = item.stat()
        name = item.name
        itemdict['name'] = name
        if item.is_file():
            itemdict['type'] = "file"
        if item.is_dir():
            itemdict['type'] = "directory"
        if item.is_symlink():
            itemdict['type'] = "symlink"
        itemlist.append(itemdict)
        
        if printtype == False:
            print(itemdict['name'])
            
        else:
            print(itemdict['name'], '--', itemdict['type'])
            
        
    results['itemlist'] = itemlist
    
    return results

def analyze(path):
# Deze functie creëert een overzicht van alle files, folders en symlinks in een bepaald path. Recursief
# Nog toe te voegen
    # Een functie voor aantal bestanden 'if directory'
    # Export naar json

    results = {'pathScanned': str(path)}
    itemlist = []
    for root, dirs, files in os.walk(path): # os.walk() geeft een overzicht terug van files en folders in iedere folder
        for item in os.scandir(root):
            itemdict = {}
            name = item.name
            result_path = item.path
            info = item.stat() # Met stat() spreek je een klasse aan die in een scandir klasse zit.
            itemdict['name'] = name
            itemdict['path'] = result_path
            if item.is_file():
                itemdict['type'] = "file"
                itemdict['size'] = info.st_size
                itemdict['lastModifiedDate'] = info.st_mtime
            if item.is_dir():
                itemdict['type'] = "directory"
            if item.is_symlink():
                itemdict['type'] = "symlink"
            itemlist.append(itemdict)

    results['itemlist'] = itemlist

    return results

def makeflat(path, destination_path = None): # Voorlopige function. Nog uit te werken
# Deze functie slaat files in subfolders plat naar één lijst van bestanden in één folder
# Gebruik deze functie als je weet dat alle files uniek geïdentificeerd zijn via hun bestandsnaam
# OPGELET! Indien destination_path = 'None', dan vindt de verwerking plaats 'in place'

    payload = analyze(path)
    files = {item for item in payload['itemlist'] if item['type'] == "file"}  # List comprehension. Te bekijken
    
def create_dirs_from_excel(path, excelpath):
    dataframe = pd.read_excel(excelpath, na_filter=False, dtype=object)
    directorylist = dataframe.to_dict('records')
    os.chdir(path)
    for directory in directorylist:
        workpath = os.path.join(path, directory['name'])
        try:
            os.makedirs(workpath, exist_ok = True) # makedirs maakt zonodig ook tussenmappen mocht dat nodig zijn.
            print("Directory '%s' created successfully" % workpath)
        except OSError as error:
            print("Directory '%s' can not be created" % workpath)

def change_dirnames_from_excel(path, excelpath): # Functie om dirs te hernoemen. 
# Specifiek handig om folders te hernoemen conform specs storage server
# Gaat uit van één excel met een kolom orig_name en new_name. Foldernamen, niet folderpaths
# Het werkt niet recursief. Slechts één niveau van folders

    dataframe = pd.read_excel(excelpath, na_filter=False, dtype=object)
    directorylist = dataframe.to_dict('records')
    os.chdir(path)
    for directory in directorylist:
        os.rename(directory['orig_name'], directory['new_name'])
        print("Directory", directory['orig_name'], "renamed in", directory['new_name'])
