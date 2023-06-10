import re
import mutuelle



import os

black_list=["de","la","par","et","le","des","à","les","au","en","du","ou",'est',"l","dans","pour","dont","soit"]

def test_by_word(text):
    
    text_split=re.findall(r"[\w']+",text)

    dico= {}
    my_list=[]


    for t in text_split:
        if  t.lower() in black_list:
            continue
        if not t.lower() in dico:
            dico[t.lower()] = 0
        dico[t.lower()] = dico[t.lower()]+ 1
        
    total = 0
    for word in dico:
        total += dico[word]

    for word in dico:
        my_list.append((word,dico[word]/total*100))
    my_list.sort(key=lambda x: x[1], reverse=True)
        
        

    print(my_list)



file = mutuelle.Files("./Contrat/etude_tarifaire_sante_logo_(1).pdf")
file="\n".join(file.parts)   
test_by_word(file)     

