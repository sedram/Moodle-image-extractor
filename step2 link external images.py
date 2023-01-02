import re
import os
from urllib.parse import unquote
remimagepath=".../Images/py/"#Make sure this path is right

findb64text = re.compile(".*<img.*base64.*")
findimage = re.compile('<img.*?>')
findsource = re.compile('src_file="(.*?)"')
findimagedata = re.compile('base64,(.*?)"')
findb64images = re.compile(".*base64.*")#findb64images = re.compile(".*base64.*src_file.*")#This assumed a src file
findendofsrc = re.compile("/([^/]*?/[^/]*?)$")
findfold = re.compile("([^/]*?)/")
findfilename = re.compile("/([^/]*?)$")
findfiletype = re.compile("image/(.*?);base64")

bcounter=1000

def use( findy, stro ):
    return findy.search(stro).groups()[0]

def killfile(x):
    if re.match(findfil, x):
        return " \n"
    else:
        return re.sub("http://...","https://...",x)#Change ... to multimedia server

with open("nof_....xml","r",encoding='utf-8') as fp, open("new_....xml","w",encoding='utf-8') as ox:#Change filenames
    alllines = fp.readlines()#each line ends with a \n
    for ind in range(len(alllines)):#only okay because I don't mess with number of lines
        if re.match(findb64text,alllines[ind]):#if the line is text and has a base64:
            imagelist=findimage.findall(alllines[ind])#I think I assume I never have a regular linked image with a base64 image
            for imago in imagelist:
                path=findsource.search(imago)
                b64maybe=findimagedata.search(imago)
                if b64maybe:
                    bcounter+=1
                    if path:#If not, there isn't a src_file for this image
                        fullsrcfile=path.groups()[0]
                        endofsrc=str(bcounter)[1:]+"_"+findfilename.search(fullsrcfile).groups()[0]
                        fold="b/"+findfold.search(findendofsrc.search(fullsrcfile).groups()[0]).groups()[0]+"/"
                    else:
                        endofsrc=str(bcounter)[1:]+"_"+"."+findfiletype.search(imago).groups()[0]
                        fold="b/"+"unk/"
                    data=b64maybe.groups()[0]
                    newline=re.sub(re.escape("data:image/"+findfiletype.search(imago).groups()[0]+";base64,"+data),remimagepath+fold+endofsrc,alllines[ind])
                    alllines[ind]=newline
    for line in alllines:
        ox.write(line)
