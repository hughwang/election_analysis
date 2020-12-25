import re
def getNext(iterator):
    try:
	    item = iterator.next()
	    return item
    except:
        return False


inputfile = 'error.txt'

with open(inputfile) as f:

    iterator = iter(f)
    while (True):
        this=next(iterator)

        if not this:
            break
        if 'Exceeded 30 redirects' in this:
            this=next(iterator)
            if this.startswith('https://static01'):
                print(this)



