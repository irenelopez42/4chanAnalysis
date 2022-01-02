import models
import json

#model tests
postJSON = {"timestamp": "1388521688", "title": None, "comment": "friendly reminder that making fun of dead nazis is perfectly acceptable\n\nhttp://en.wikipedia.org/wiki/Ian_Stuart_Donaldson\n\nhttps://www.youtube.com/watch?v=c7iIjJVyLmk"}
parsedPost = models.ChanPost(id=24851906,json=postJSON)
print(parsedPost)

exampleFile = "exampleThreads.json"
with open(exampleFile,"r") as file:
    threads_json = json.load(file)
parsedThreads = models.ChanThread.parseThreads(threads_json)
posts = parsedThreads[0].asRawStrings()
print(posts[:3])