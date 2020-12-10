# Step 1 - Generate file with documentation pageg
1. Documents.yml contains a list of documents in Juniper documentation that were used for for the last update of documentation.
1. Open Documents.yml file. Update links to the documents with latest version, and add new ones. Documents that were removed by Juniper should stay in the file as the script will later mark them as deleted.
1. Run ```JuniperDocDiff.py -i documents.yml -o output.yml``` 
1. Compare output file with the previous version that exists in repo   
1. Comment the changes:
    1. if the url was removed: investigate with TSC / community should it be rmoved from TF documentation as well
    1. if the url was added: check with Juniper representative if that is something that can be copied to TF. If yes then JuniperAgreesToCopy=True otherwise JuniperAgreesToCopy=false
1. Compare files names and copy JuniperAgreesToCopy field for mathing pages. This will ensure that Juniper's agreement to use those pages will be preserved.

Result: you have a file that contains:
1. List of links to pages of the lates documentation version prepared by Juniper
1. Information which of those pages can be copied to TF

# Step 2 - Get all pages and check for difference
1. Run ```webcrawler -i output.yml``` 
1. The script will download all files under the links provided in output.yml
1. The script will download only tiles marked as JuniperAgreesToCopy=True
1. Create new branch outof docs master
1. Commit ```documentation_pages_output/``` to that branch
1. Raise pull request of that branch to master
1. Compare changes in the files.
1. Analyze each change and update TF documentation
1. In case new image file appeared ask TSC / Community to prepare same screenshot with TF logo

