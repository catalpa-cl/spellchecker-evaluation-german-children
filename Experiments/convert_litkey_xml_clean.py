"""
Transform the CLEANED Litkey Corpus (XML) into the spelling-XML-file format
If orig and target differ, it is tagged as e.g. <error correct="Fenster" type="ins_V">Fnster</error>

See paper with Experiments for how the corpus is cleaned

"""

import xml.etree.ElementTree as ET
import re
import os

corpus_path = "corpora/litkey-xml/"

#root element for our spelling-XML with corpus name as attribute
corpus = ET.Element("corpus")
corpus.set("name", "Litkey_Clean")


for file in sorted(os.listdir(corpus_path)):


    #if not file.startswith("06-232"):  continue #check single file (01-140)
    tree = ET.parse(corpus_path+"/"+file)
    root = tree.getroot()

    # initialize collection of correct tokens at the beginning of a text
    # create sub element for each text with text ID as attribute
    text = ET.SubElement(corpus, "text")
    text.set("id", re.sub("\.xml", "", file))
    text.set("lang", "de")
    text.text = None

    # collects all XML elements that contain our spelling error markups
    errorlist = []

    index = 0

    while index < len(root.findall("token")):
        token = root.findall("token")[index]
        orig = token.get("orig")
        target = token.get("target")
        
        
        #remove dashes at linebreaks
        if "-" in orig:
            
            characters_orig =  token.find("characters_orig")
            
            for char_o in characters_orig:
                    try:
                        if char_o.get("layout") == "EOL":
                            if char_o.text == "-":
                                o_index = int(char_o.get("id").lstrip("o"))-1
                                if o_index < len(orig)-1: #keep dashes at the end of the word
                                    orig = orig[0 : o_index : ] + orig[o_index + 1 : :]
                            else: #dash after linebreak
                                o_index = int(char_o.get("id").lstrip("o"))
                                if orig[o_index] == "-":
                                    orig = orig[0 : o_index : ] + orig[o_index + 1 : :]
                                           
                    except:
                        continue
        
        
        
        
        
        orig = re.sub("_", "", orig)  # remove _
        orig = re.sub("\|", "", orig) # remove |
                
        
        
        #ignore certain tokens
        if orig.lower() != target.lower() \
           and not token.get("target_comments")  in ["unclear/onom", "ungram"] \
           and not  "*" in orig \
           and not re.search(r'Lea|Lars|Dodo|lea|lars|dodo',target) \
           and not "." in target \
           and re.search(r'[A-Za-zÄÖÜäöüß]{2,}', target):
                   
            
            split_error_list = []
            split_error_list.extend([err.get("cat_fine") for errors in token.findall("errors") for err in errors.findall("err")])
            
            error = ET.Element("error")
            error.set("correct", target)
            error.set("type", ",".join(split_error_list))

            error.text = orig
            error.tail = " "


            errorlist.append(error)
            index += 1


        else:
            if len(errorlist) == 0 and text.text != None:
                text.text += orig + " "
            elif len(errorlist) == 0 and text.text == None:
                text.text = orig + " "
            else:
                if errorlist[-1].tail != None:
                    errorlist[-1].tail += orig + " "
                else:
                    errorlist[-1].tail = orig + " "
            index += 1

    for elem in errorlist:
        text.append(elem)

corpus_tree = ET.ElementTree(corpus)
corpus_tree.write("corpora_spelling/litkey_spelling_clean.xml", encoding="unicode")



