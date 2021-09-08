bibMain_fp = "mybib.bib"
bibToAdd_fp = "../PentacenePaper/GitRepo/myBib.bib"


def read_bib(fp):
    with open(fp, 'r') as f:
        ltxt = [i for i in f.read().split('@') if i.count('{') == i.count('}') and '{' in i]
    return ltxt


def getObjNames(bib):
    return [i[i.find('{')+1:i.find(',')].strip() for i in bib]


def getArtByNames(bib, names):
    namesInBib = getObjNames(bib)

    bibItems = []
    for i, name in enumerate(namesInBib):
        if name in names:
            bibItems.append('@'+bib[i])

    return bibItems


mainBib = read_bib(bibMain_fp)
bibToAdd = read_bib(bibToAdd_fp)

artMain = set(getObjNames(mainBib))
artToAdd = set(getObjNames(bibToAdd))
# Get names that aren't in the main bib and need to be added
artToUpdate = artToAdd - artMain
print(f"Adding {len(artToUpdate)} entries to the file '{bibMain_fp}'")
print("These are: \n\t*"+'\n\t*'.join(artToUpdate))

newBibItems = getArtByNames(bibToAdd, artToUpdate)

with open(bibMain_fp, 'r') as f:
    bibTxt = f.read()
newBibTxt = ''.join(newBibItems) + bibTxt
with open(bibMain_fp, 'w') as f:
    f.write(newBibTxt)

