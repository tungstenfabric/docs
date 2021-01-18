import os
import argparse, textwrap
import re 

import pprint


class DeContralizeDocument(object):
    def __init__(self):
        self.newDocumentText = []
        self.decontralize()

    def decontralize(self):
        pp = pprint.PrettyPrinter(indent=4)

        #open file
        t = open(args.textFile, "r+")
        #load content
        content=t.read()

        #open dictionary
        d = open(args.dictionary, "r")
        print("Looking for: [Cc]ontrail( |:|\\n|\.)")
        print("Occurences found: "+str(len(re.findall("[Cc]ontrail( |:|\n|\.)",content)))+"")
        print("Among them:")
        #for each line
        for line in d:
            #split by >>
            fromto=line.split(">>")
            #if there is no subtitution in the dictionary file then skip that line
            if len(fromto) < 2:
                continue
            #trim first cell
            fromto[0]=fromto[0].strip()
            #trim second cell
            fromto[1]=fromto[1].strip()

            #if there are more than zero occurences then show the number
            if content.count(fromto[0])>0:
                print(str(content.count(fromto[0]))+" "+fromto[0])
            #if marked as manually then skip it
            if "manually" in str(fromto[1]):
                continue
            #do a replacement
            #TEST VALUES
            #content="ddsdsd ds d s Contrail manifests: Contrail manifests Contrail\nmanifests:"
            #fromto[0]="Contrail manifests"
            #fromto[1]="TEEEEST manifests"
            #look for patterns that end with space, colon, new line, or full stop as we don't want to replace things that might be a source code or CLI commands.
            content=re.sub("{}(?=( |:|\n|.))".format(fromto[0]),fromto[1],content)
        print("\nOccurences left: "+str(len(re.findall("[Cc]ontrail( |:|\n|\.)",content)))+"\n")
        #remove obsolete HTML tags
        #content=re.sub(".*raw:: html\n\n.*<(div|/div)[a-zA-z =\"-]*>","",content)
        #write down the new file
        t.seek(0, 0)
        t.write(str(content))              
        t.close()
        d.close()
        
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script takes input two files: one with de-contralization guidance and one where those words need to be replaced. As a result it will save the same file with new content.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d','--dictionary', help=textwrap.dedent('''\
        dictionary that contain guidance what and how should be replaced. The defualt decontralization_guide.txt can be found in this repo.
        '''),
        required=True)
    parser.add_argument('-t','--textFile',help='File that needs to be de-contralized', required=True)
    args = parser.parse_args()

    DeContralizeDocument()