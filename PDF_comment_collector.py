# Script to collect all comments from PDF files in different folders,
# which are stored in a txt-file and can searched for with a 'search' function

# packages:
import fitz
import os
from datetime import date

def pdf_comment_collector(root, file):
    """This will take a root and a text file"""
    """And search all pdfs within root"""
    """Then it will print these to the txt file"""
    list_of_pdfs = []
    list_of_lists = []
    no_PDFs = []
    no_comments = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            path1 = os.path.join(path, name)
            path2 = path1.replace("\\", "/")
            list_of_pdfs.append(path2)
            
    c = file
    f = open(c, 'a') # open list in 'append' mode
    
    # iterate through all pfds and append them to a list
    # for each pdf it will go through all pages and append comments to a new list
    # in case of docs =! pdfs, it will pass and append the doc name to list
    
    for pdf in list_of_pdfs:
        file_list = [] 
        if "pdf" not in pdf:
            no_PDFs.append(pdf)
        else: 
            doc = fitz.open(pdf, filetype="pdf") #can it be opened?
            #print(doc)
            file_list.append(str(pdf))
        
            for i in range(doc.pageCount):
                page = doc[i]
                for annot in page.annots():
                    annoted = annot.info["content"]
                    #print(type(annoted))
                    #print(annot)
                    #print(annoted)
                    if annoted:
                        if "\r" in annoted:
                            new_annoted = annoted.replace("\r", "") 
                            file_list.append(new_annoted)
                        else:
                            file_list.append(annoted)
                    else:
                        no_comments.append(annoted)

            list_of_lists.append(file_list)
            
    print(f"list of lists: {list_of_lists}")
    print(f"no comments: {no_comments}")
    print(f"no pdfs: {no_PDFs}")
    

    # now we have a list of lists
    # here each pdf (which is an entry in the list_of_list)
    # is iterated through and pdf name and path are written in the txt doc
    # then the comments (in the second list) are iterated through and
    # are written into the txt document
    f.writelines(f"{date.today()}\nBeginning of search:\n")
    for elem in list_of_lists[:-1]:
        for item in elem[:-1]:
            f.writelines(f"{item}\n")
        for item in elem[-1:]:
            f.writelines(f"{item}\n\n")

    for elem in list_of_lists[-1:]:
        for item in elem[:-1]:
            f.writelines(f"{item}\n")
        for item in elem[-1:]:
            f.writelines(f"{item}\n\n")
            f.writelines(f"end of search from {date.today()}\n\n")
        #print(item)

# this is the call for the function
# here the root of the folder structure has to be assigned,
# and as second argument the name of the txt file has to be given
pdf_comment_collector("D:/Paper", "D:/paper/all_pdf_comments.txt")