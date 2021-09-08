import re

bibRef = "/home/matt/Documents/PhD/PentacenePaper/GitRepo FirstEdit/myBib.bib"
bibChange = "./mybib.bib"

class BibTex(dict):

    def __init__(self, fn):
        self.fn = fn

        self.open_read(fn)
        self.parse()

    def open_read(self, fn):
        with open(fn, 'r') as f:
            self.ftxt = f.read()

    def parse(self):
        allID = re.findall("@.*{.*,", self.ftxt)
        for i in allID:
            start_ind = self.ftxt.find(i)
            artTxt = self.ftxt[start_ind:]

            # Get just the article text
            brackInd = artTxt.find("{")
            end_ind = self._get_closing_bracket(artTxt, brackInd)
            artTxt = artTxt[:end_ind]

            # Get the ID
            ID = artTxt[artTxt.find('{')+1: artTxt.find(",")]
            self[ID] = artTxt

    def _get_closing_bracket(self, txt, start_ind, brack='{'):
        count = 0
        brackChanges = {'{':1, '}':-1}
        for i, c in enumerate(txt[start_ind:]):
            count += brackChanges.get(c, 0)
            if count == 0:
                return start_ind + i +1

        raise SystemExit("Couldn't find closing bracket")


    def write(self, fn):
        with open(fn, 'w') as f:
            ftxt = ""
            for key in self:
                ftxt += "%s\n\n" % self[key]
            f.write(ftxt)

refBib = BibTex(bibRef)
bibToChange = BibTex(bibChange)

bibToChange.update(refBib)
bibToChange.write("tmp.bib")
