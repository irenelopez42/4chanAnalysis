import datetime

#define relevant models for the analysis here
class ChanPost:
    id = None
    date = None
    title = None
    comment = None
    message = None

    def __init__(self, id: int, json, date: datetime.datetime = None) -> None:
        """Take a json representation of a post and use it to initialize a new ChanPost object"""
        self.id = id
        try:
            self.date = datetime.datetime.fromtimestamp(float(json['timestamp']))
        except:
            self.date = date
        
        try:
            self.title = "" if json['title'] is None else json['title']
        except:
            self.title = ""

        try:
            self.comment = "" if json['comment'] is None else json['comment']
        except:
            self.comment = ""

        try:
            self.message = "" if json['message'] is None else json['message']
        except:
            self.message = ""

    def __str__(self) -> str:
        return f"Title: {self.title}\nDate: {self.date}\nMessage: {self.message}\nComment: {self.comment}"

    def asRawString(self) -> tuple[int, datetime.datetime, str]:
        """Returns a tuple of ID, date and all text contained in the post"""
        return (self.id, self.date, " ".join((self.title,self.comment,self.message)))

class ChanThread:
    post = None
    replies = list()

    def __init__(self, id: int, json) -> None:
        """Take a json representation of a thread and use it to initialize a new ChanThread object"""
        self.post = ChanPost(id=id,json=json['op'])
        for rep in json['replies']:
            self.addReply(rep, json=json)

    def __str__(self) -> str:
        res = f"Original Post: {self.post}\nReplies:\n"
        return res + "\n".join(map(str, self.replies))

    def addReply(self, text: str, **json) -> None:
        """Add a post as reply to this thread. IDs of replies are set by incrementing the thread id"""
        altered = json.copy()
        altered['message'] = text
        replyId = self.post.id + len(self.replies) + 1
        self.replies.append(ChanPost(id=replyId, json=altered, date=self.post.date))

    def asPosts(self):
        """Return this thread's post and all replies in a list"""
        return ([self.post] if self.post is not None else []) + self.replies

    def asRawStrings(self):
        """Return a list of ID,date,text tuples"""
        return list(map(ChanPost.asRawString, self.asPosts()))

    def parseThreads(json):
        return list(map(lambda item: ChanThread(int(item[0]),json=item[1]), json.items()))