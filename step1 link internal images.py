import re
import os
from urllib.parse import unquote
remimagepath=".../Images/py/"#Make sure this path is right

findfil = re.compile('<file name="(.*?)"')
wholeplugin = re.compile('"(@@PLUGINFILE@@/.*?)[\?"]')#I need to use [\?"] instead of " because some images have extraneous ?time=154... parts.

listoffs={}
fcounter=100
#bcounter=1000

def notef(index):
    if index not in listoffs:
        global fcounter
        fcounter+=1
        listoffs[index]=fcounter

def use( findy, stro ):
    return findy.search(stro).groups()[0]

def killfile(x):
    if re.match(findfil, x):
        return " \n"
    else:
        return re.sub("http://...","https://...",x)#Change ... to multimedia server

with open("...ex.xml","r",encoding='utf-8') as fp, open("...out.xml","w",encoding='utf-8') as ox:#Change filenames
    alllines = fp.readlines()#each line ends with a \n
    for ind in range(len(alllines)):#only okay because I don't mess with number of lines
        if re.match(findfil,alllines[ind]):#if the line has a <file:
            notef(ind)
        while (plaggy := wholeplugin.search(alllines[ind])):#while line has pluginfile and I capture it:
            pluggy=plaggy.groups()[0]
            foundimage=False
            tempind=ind
            while not foundimage:
                tempind+=1
                print(tempind)#fordebug
                if re.match(findfil,alllines[tempind]):#any <file there?
                    notef(tempind)#add the tempind to a list of <file lines and increase counter if I did so
                    if unquote(pluggy[15:]) == use(findfil,alllines[tempind]):#if file is correct:
                        foundimage=True
                        #alllines[ind]=re.sub(pluggy,remimagepath+"f/"+str(listoffs[tempind])[1:]+"_"+pluggy[15:],alllines[ind])#replace filename
                        alllines[ind]=re.sub(pluggy,remimagepath+str(listoffs[tempind])[1:]+"_"+pluggy[15:],alllines[ind])#replace filename
    #By now I've fixed all the pluginfiles
    #Just trying to kill the <files
    print(listoffs)# for debug purposes
    for line in map(killfile,alllines):
        ox.write(line)
