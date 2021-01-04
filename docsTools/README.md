# Step 1 - Generate file with documentation pageg
1. Documents.yml contains a list of documents in Juniper documentation that were used for for the last update of documentation.
1. Open Documents.yml file. Update links to the documents with latest version, and add new ones. Documents that were removed by Juniper should stay in the file as the script will later mark them as deleted.
1. Run ```JuniperDocDiff.py -i documents.yml -o output.yml``` 
1. Compare output file with the previous version that exists in the docTools repo   
1. Comment the changes:
    1. if the url was removed: investigate with TSC / community should it be rmoved from TF documentation as well
    1. if the url was added: check with Juniper representative if that is something that can be copied to TF. If yes then JuniperAgreesToCopy=True otherwise JuniperAgreesToCopy=false
1. Compare files names and copy JuniperAgreesToCopy field for mathing pages. This will ensure that Juniper's agreement to use those pages will be preserved.
1. Commit the output file with a flag ```-m "<RELEASE NAME>```. For example for release r2020 it will be ```-m "r2020"```

Result: you have a file that contains:
1. List of links to pages of the latest documentation version prepared by Juniper
1. Information which of those pages can be copied to TF

# Step 2 - Get all pages and check for difference
1. Download documentation_pages_output folder from the docTools repo. This is the previous iteration of document files.
1. Run ```python3 WebCrawler.py -i output.yml -o documentation_pages_output``` 
1. The script will download all files under the links provided in output.yml
1. The script will download only tiles marked as JuniperAgreesToCopy=True
1. All existing files and images will be overwritten with new version. 
1. Pages and images that don't exists in the new documentation will be left untouched.
1. Compare changes in .rst files generated inside documentation_pages_output folder:
    1. If something was changed, look up the same file in docs repo and see if corrections are needed
1. For images:
    1. Manually check all changed ones with their previous version. Sometime you will get false-positive because change that is not visible to a user (for example in EXIF fields) will be treated as a change by git.
    1. In case new image was added use ```grep -r "<FILE_NAME" *``` to find document in which that image was used. For example: ```grep -r "s041998.gif" *```. Open that document and make same screenshot using Tungsten Fabric. If you don't have access to lates version of TF ask community to provide such image.
1. Commit ```documentation_pages_output``` with a flag ```-m "<RELEASE NAME>```. For example for release r2020 it will be ```-m "r2020"```
1. Commit any changes done to docs with a flag ```-m "<RELEASE NAME>```. For example for release r2020 it will be ```-m "r2020"```
