import re
import base64
import os
from bs4 import BeautifulSoup
lclimagepath=".../"#Make sure this path is right
if not os.path.exists(lclimagepath):
    os.makedirs(lclimagepath)

fcounter=100
bcounter=1000

findimage = re.compile('<img.*?>')
findsource = re.compile('src_file="(.*?)"')
findimagedata = re.compile('base64,(.*?)"')
findb64images = re.compile(".*base64.*")#findb64images = re.compile(".*base64.*src_file.*")#This assumed a src file
findendofsrc = re.compile("/([^/]*?/[^/]*?)$")
findfold = re.compile("([^/]*?)/")
findfilename = re.compile("/([^/]*?)$")
findfiletype = re.compile("image/(.*?);base64")

def use( findy, stro ):
    return findy.search(stro).groups()[0]

def shortname( isfile, name ):#name should be .png or something when not file
    if isfile:
        global fcounter
        fcounter+=1
        return "f/"+str(fcounter)[1:]+"_"+name
    else:
        global bcounter #need "global" to modify in functions
        bcounter+=1
        return str(bcounter)[1:]+"_"+name

def use( findy, stro ):
    return findy.search(stro).groups()[0]



with open("cm2ex.xml","r",encoding='utf-8') as fp, open("cm2out.tsv","w",encoding='utf-8') as outHandler:
#with allows me not to close the things manually
    soup = BeautifulSoup(fp, "xml")

    if not os.path.exists(lclimagepath+"f/"):
        os.makedirs(lclimagepath+"f/")
    
    fileitems=soup.find_all("file",{"encoding" : "base64"}, limit=100000)#Note limit for safety
    for thing in fileitems:
        cat=thing.find_previous("question",{"type" : "category"}).stripped_strings
        fullsrcfile=thing['name']#hope this never errors...
        shortsrc = shortname(True, fullsrcfile)
        for data in thing.stripped_strings:
            with open(lclimagepath+shortsrc,"wb") as file:
                file.write(base64.b64decode(data))
        for stry in cat:
            outHandler.write(stry+"\t"+fullsrcfile+"\t"+lclimagepath+shortsrc+"\n")

    if not os.path.exists(lclimagepath+"b/"):
        os.makedirs(lclimagepath+"b/")
    
    imageitems=soup.find_all("text",string=findb64images, limit=100000)#Note limit for safety
    for thing in imageitems:
        cat=thing.find_previous("question",{"type" : "category"}).stripped_strings
        for um in thing.stripped_strings:
            imagelist=findimage.findall(um)
            for imago in imagelist:
                path=findsource.search(imago)
                if path:#If not, there isn't a src_file for this image
                    fullsrcfile=path.groups()[0]
                    endofsrc=shortname(False, findfilename.search(fullsrcfile).groups()[0])
                    fold="b/"+findfold.search(findendofsrc.search(fullsrcfile).groups()[0]).groups()[0]+"/"
                else:
                    #print("wow")
                    fullsrcfile="NA"
                    endofsrc=shortname(False, "."+findfiletype.search(imago).groups()[0])
                    fold="b/"+"unk/"
                if not os.path.exists(lclimagepath+fold):
                    os.makedirs(lclimagepath+fold)
                b64maybe=findimagedata.search(imago)
                if b64maybe:
                    data=b64maybe.groups()[0]
                    #print(fold)
                    with open(lclimagepath+fold+endofsrc,"wb") as file:
                        file.write(base64.b64decode(data))
                for stry in cat:
                    outHandler.write(stry+"\t"+fullsrcfile+"\t"+lclimagepath+fold+endofsrc+"\n")

