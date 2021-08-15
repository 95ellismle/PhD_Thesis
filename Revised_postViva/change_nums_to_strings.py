num_map = {str(i): j for i, j in enumerate(('zero', 'one', 'two',
                                            'three', 'four',
                                            'five', 'six', 'seven',
                                            'eight', 'nine', 'ten',
                                            'eleven', 'twelve',
                                            'thirteen',
                                            'fourteen', 'fifteen'))}


import re


fn = "CTMQC_Applied_To_Tully_Models.tex"


with open(fn, 'r') as f:
    txt = f.read()


quantity_identifiers = {'of'}

allOcc = re.findall(" [a-z,]* [0-9] [,a-z]* ", txt)
for i in allOcc:
    splitter = i.split()
    num_wrd = splitter[1]

    cond = splitter[0].lower() not in quantity_identifiers
    cond += splitter[0].lower() == 'of' and splitter[2] == 'atom'
    if cond:
        num_wrd = num_map.get(splitter[1], splitter[1])

    if splitter[1] != num_wrd:
        splitter[1] = r"\mremove{"+splitter[1]+r"}\madd{"+num_wrd+"}"
    print(f"{txt.find(i)}: {' '.join(splitter)}")

    repl_txt = ' ' + ' '.join(splitter) + ' '

    if i in txt:
        txt = txt.replace(i, repl_txt)


#with open(fn.split('.')[0] + "_1.tex", 'w') as f:
with open(fn, 'w') as f:
    f.write(txt)



