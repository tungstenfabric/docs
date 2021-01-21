# Step 1 - Generate a file with documentation pages
1. Documents.yml contains a list of documents in a Juniper documentation. 
1. Open Documents.yml file. Update links to the documents with the latest version and add any new ones. Documents that were removed by Juniper should stay in the file as the script will later mark them as deleted.
1. Run ```JuniperDocDiff.py -i documents.yml -o output.yml``` 
1. Compare the output file with the previous version that exists in the docTools repo 
1. Comment on the changes:
   1. if the URL was removed: investigate with TSC / community should it be removed from TF documentation as well
   1. if the URL was added: check with Juniper representative if TF can use that. If yes then change ``JuniperAgreesToCopy=True`` otherwise `JuniperAgreesToCopy=false`
1. Compare file names and copy JuniperAgreesToCopy field for matching pages. That will preserve Juniper's agreement to use those pages.
1. Commit the output file with a flag ```-m "<RELEASE NAME>```. For example, for release r2020 it will be ```-m "r2020"```

Result: you have a file that contains:
1. List of links to pages of the latest documentation version prepared by Juniper
1. Information which of those pages can be used by TF

# Step 2 - Get all pages and check for the difference
1. Download documentation_pages_output folder from the docTools repo. It is the previous iteration of document files.
1. Run ```python3 WebCrawler.py -i output.yml -o documentation_pages_output``` 
1. The script will download all files under the links provided in output.yml
1. The script will download only tiles marked as JuniperAgreesToCopy=True
1. Script will overwrite all existing files and images with the new version. 
1. Pages and images that don't exist in the new documentation will be left untouched.
1. Compare changes in .rst files generated inside documentation_pages_output folder. 
1. For changed files:
   1. Look up the same file in docs repo and see if corrections are needed.
1. For new files:
   1. If it's a new file in new folder then create new folder in root folder of docs repo
   1. Folder name should be written using *kebab-case* naming convention
   1. Inside that folder put index.rst file that will contain toc tree mentioning your new file. Use index.rst from root folder as an example
   1. In root folder of docs, in index.rst file in toc tree section add reference to your new index.rst
   1. Search for any mentions of Contrail ```grep  -rho "[cC]ontrail-[^ ,'\"\:\{\)\.\;\`/]*\|[cC]ontrail [a-zA-Z]* [a-zA-Z]*" --exclude=\*.{md,html,css} * > occurences.txt```
   1. Check in what files they appear using grep. For example: ```grep  -r "Contrail vRouter Next" --exclude=\*.{md,html,css,txt} docsTools/*```
   1. Use ```decontralize.py``` script to de-contralize document and to remove obsolete newlines and html tags.
   1. Replace admonitions like ```**NOTES**``` ```**CAUTION**``` with rst admonitions like ```.. notes::```
   1. Correct internal hyperlinks to headers using ``` `header text`_ ```
   1. Remove internal hyperlinks to elements that cannot be hyperlinked in RST (for example hyperlinks to bullet points)
   1. Correct or remove hyperlinks to external documents
   1. After de-contralization run the search again for any Contrail references. Correct them manually.
1. For all images:
   1. Manually check all changed ones with their previous version. Sometimes you will get false-positive because a change that is not visible to a user (for example, in EXIF fields) will be treated as a change by git.
   1. In case a new image was added, use ```grep -r "<FILE_NAME" *``` to find the document in which that image was used. For example: ```grep -r "s041998.gif" *```. Open that document and make the same screenshot using Tungsten Fabric. If you don't have access to the latest TF version, ask community members for help.
1. Run ```tox -d docs``` to see if there are no errors in your new file
1. Commit ```documentation_pages_output``` with a flag ```-m "<RELEASE NAME>```. For example for release r2020 it will be ```-m "r2020"```
1. Commit any changes done to docs with a flag ```-m "<RELEASE NAME>```. For example, for release r2020 it will be ```-m "r2020"```

