import yaml
import json
import urllib.request
from urllib.parse import urlparse
import os
import argparse, textwrap
import re 
from bs4 import BeautifulSoup
import yaml

def read_input_file():
    with open(args.input) as input:
        print("Opened yaml")
        return yaml.safe_load(input)
            


class AllDocuments(object):
    def __init__(self, documents_dict):
        #self.config = config
        # set of DOCUMENTS with dictionaries of PAGES 
        self.newDocuments = []
        self.generateDocuments(documents_dict)

    def generateDocuments(self, documents):
        for document in documents:
            pages=[] #list of pages in that document
            print('Analyzing '+document['name'])
            websiteName=document['name']
            websiteURL=document['url']
            try:
                websiteCode = urllib.request.urlopen(websiteURL).read() #kod html strony z ToC
            except:
                print("Page doesn't exist: "+websiteURL)
                continue
            filename=os.path.basename(urlparse(websiteURL).path) #nazwa pliku z ToC aby usunąć go z URL
            websiteBaseUrl=websiteURL.replace(filename, "") #domena do której będą doklejane linki z ToC
            #print('3 '+websiteBaseUrl)
            
            html = websiteCode #the HTML code you've written above
            parsed_html = BeautifulSoup(html, 'html.parser')
            ToC=parsed_html.body.find(id="pwpsList") #extract LI element containing ToC
            ToCLinks=ToC.find_all('a') #extract list of A tags with links
            id=0
            for link in ToCLinks:
                id=id+1
                #exctract href and join it with base url
                #page['url']=websiteBaseUrl+link.attrs['href']
                #print(websiteBaseUrl+link.attrs['href'])
                #add ID numer
                #page['id']=print(id)
                #add EMPTY JuniperAgreesToCopy
                #page['JuniperAgreesToCopy']=''
                #append to dictionary of pages
                page=dict([('url', websiteBaseUrl+link.attrs['href']), ('id', id), ('juniperAgreesToCopy', False),('fileName',link.attrs['href'])])
                pages.append(page)
            #create new document with old attributes and pages
            newDocument=dict([('name', websiteName), ('url', websiteURL), ('pages', pages),('filename',filename)])
            #print(newDocument)
            #print(yaml.dump(newDocument))
            self.newDocuments.append(newDocument)
            #print(newDocument)
        #write everything down to a file
        self.writeDownNewYAML(self.newDocuments)

    def writeDownNewYAML(self, document):
        #write down to file
        print("Writing to yaml")
        with open(args.output, 'w') as file:
            documents = yaml.dump(document, file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script takes input file with links to top level of each document in Juniper documentation and for each of those documents he gathers link to every page.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--input', help=textwrap.dedent('''\
        YAML file containint links to root level of each document mentioned in Juniper documentation direcetory
        File format:
            - name: <<name of the first document>>
              url: <<URL of the first document>>
            - name: <<name of the second document>>
              url: <<URL of the seconddocument>>
        Example:
            - name: Contrail Networking and Security User Guide
              url: https://www.juniper.net/documentation/en_US/contrail20/information-products/pathway-pages/contrail-networking-security-user-guide.html
        '''),
        required=True)
    parser.add_argument('-o','--output',help='Output file that should be compared with the output file generated for previous version to see what have changed', required=True)
    args = parser.parse_args()
 

    input = read_input_file()
    #print("Loaded input")
    AllDocuments(input['documents'])