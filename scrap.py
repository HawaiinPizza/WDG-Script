import requests
import pickle
import re
# Thank god this comes incldued wtih python.
from html.parser import HTMLParser
def findwdg(catalog)->(dict):
    """ Returns the replies of a thread with wdg in it"""
    for page in catalog.json():
        for thread in page["threads"]:
            if("sub" in thread):
                if("/wdg/" in thread["sub"]):
                    threadnum = thread["no"]
                    return (requests.get(f"https://a.4cdn.org/g/thread/{threadnum}.json"))

    
# thread = findwdg()

# res=findwdg(data)

# data=requests.get("https://a.4cdn.org/g/catalog.json")
# res = findwdg(data)
# with open("DATA", "wb") as f:
#     pickle.dump(res, f)

res = []
with open("DATA", "rb") as f:
    res = pickle.load(f)



testme = res.json()["posts"][-1]

class MyHTMLParser(HTMLParser):
    """Get the html from any posts that DOES have title: and progress:, and returns the acutal text"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.data=""
    def handle_data(self, data):
        self.data+=data
    def handle_starttag(self,tag, attrs):
        if(tag=="br"):
            self.data+="\n"
    def pop(self):
        tmp = self.data
        self.data=""
        return tmp
p = MyHTMLParser()

def parsepost(post):
    regex = re.compile("title:.*\n|progress:.*\n")
    if(regex.search(post)!=None):
        print("FOUND CORRECT ONE!")
        print(post)
        # print(post)

# p.feed(testme["com"])
# parsepost(p.data,True)

for i in res.json()["posts"]:
    p.feed(i["com"])
    parsepost(p.pop())
    p.close()



# README IF THIS ISNT WORKING
# You might not have DATA file. Check the pastpin link shown here 
