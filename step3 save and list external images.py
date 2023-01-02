import re
import base64
import os
import requests
from bs4 import BeautifulSoup
lclimagepath=".../"#Make sure this path is right
if not os.path.exists(lclimagepath):
    os.makedirs(lclimagepath)

maxlimit=10#low first for safety
#maxlimit=100000#high for completeness

fcounter=100
bcounter=1000

findimage = re.compile('<img.*?>')
findendofsrc = re.compile("/([^/]*?/[^/]*?)$")
findfold = re.compile("([^/]*?)/")
findfilename = re.compile("/([^/]*?)$")
findfiletype = re.compile("image/(.*?);base64")

def use( findy, stro ):
    return findy.search(stro).groups()[0]

def shortname( isfile, name ):#name should be .png or something when not file
    global fcounter
    fcounter+=1
    return str(fcounter)[1:]+"_"+name
    
def use( findy, stro ):
    return findy.search(stro).groups()[0]



with open("...out....xml","r",encoding='utf-8') as fp, open("...out....tsv","w",encoding='utf-8') as outHandler:#update filenames
#with allows me not to close the things manually
    soup = BeautifulSoup(fp, "xml")

    if not os.path.exists(lclimagepath+"f/"):
        os.makedirs(lclimagepath+"f/")
    
    fileitems=soup.find_all("file",{"encoding" : "base64"}, limit=maxlimit)
    for thing in fileitems:
        cat=thing.find_previous("question",{"type" : "category"}).stripped_strings
        fullsrcfile=thing['name']#hope this never errors...
        shortsrc = shortname(True, fullsrcfile)
        for data in thing.stripped_strings:
            with open(lclimagepath+shortsrc,"wb") as file:
                file.write(base64.b64decode(data))
        for stry in cat:
            outHandler.write(stry+"\t"+fullsrcfile+"\t"+lclimagepath+shortsrc+"\n")
