import re
def getNext(iterator):
    try:
	    item = iterator.next()
	    return item
    except:
        return False


inputfile = 'repSenator.txt'
outputfile = 'repSenator.csv'
with open(inputfile) as f, open(outputfile,"w") as w:
    w.write("id,title,name,email\n")
    iterator = iter(f)
    while (True):
        this=next(iterator)

        if not this:
            break
        if this[0].isdigit():

            results=re.split('\s+', this)
            id=results[0].replace(".","")
            title=results[1]
            name=results[2]
            email = next(iterator).rstrip()

            print(id, title, name, email)
            w.write(f"{id},{title},{name},{email}\n")
            empty = next(iterator)

