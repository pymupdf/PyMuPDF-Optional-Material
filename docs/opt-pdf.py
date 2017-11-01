from __future__ import print_function
import fitz
import os

fn = "PyMuPDF.pdf"

ba = open(fn, "rb").read()
oldsize = len(ba) / 1024.0
doc = fitz.open("pdf", ba)
toc = doc.getToC(False)
for page in reversed(doc):
    if page.getText().startswith("INDEX\n"):
        toc.append([1, "INDEX", page.number + 1])
        break
toc.insert(0, [1, "PyMuPDF Documentation", 1])
doc.setToC(toc)

m = doc.metadata
m["author"] = "Jorj X. McKie"
m["keywords"] = "PDF, XPS, EPUB, CBZ, fitz"
m["subject"] = "Version 1.11"
m["title"] = "PyMuPDF Documentation"
doc.setMetadata(m)

doc.save(fn, garbage = 4, deflate = True, clean = True)
doc.close()
newsize = os.stat(fn).st_size / 1024.0
print("Sizes (KB), old:", str(round(oldsize, 2)), "new:", str(round(newsize, 2)),
      "change:", str(round(oldsize - newsize, 2)))