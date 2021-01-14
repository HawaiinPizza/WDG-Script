import requests
import pickle
import re
import db
# Thank god this comes incldued wtih python.
from html.parser import HTMLParser
def findwdg()->(dict):
    """ Returns the replies of a thread with wdg in it"""
    catalog=requests.get("https://a.4cdn.org/g/catalog.json")
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

def parsepost(post):
    """ Given a post, try to parse out the relevant columsn, as listed below """
    regex = re.compile("title:.*\n|progress:.*\n")
    if(regex.search(post)!=None):
        # print(regex.findall(post))

        regexstring=''.join(map(lambda i: i+":.*\\n|", db.columns))
        regexstring = regexstring[0:-3]
        # print(regexstring)
        regex2 = re.compile(regexstring)
        flags=(regex2.findall(post))
        ans = {}
        for flag in flags:
            (column, data) = flag.split(":", 1)
            ans[column]=data.replace("\n", "")
        return ans
    return None




def main():
    """
    For testing
    res = []
    with open("DATA", "rb") as f:
        res = pickle.load(f)
    testme = res.json()["posts"][-1]
    """
    wdgPosts = findwdg()
    p = MyHTMLParser()
    for i in wdgPosts.json()["posts"]:
        p.feed(i["com"])
        parsedpost=parsepost(p.pop())
        if(parsedpost!=None):
            db.init()
            db.insertentry(parsedpost)
        p.close()
    list(map(lambda i:print(i), db.getall()))
main()
