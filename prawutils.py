import praw
import string
import markovutils

UserAgent = "mac:VoiceofReddit:v0.1 (by /u/tbasherizer)"

comments = []


class PrawkovSession:

    def __init__(self,markovdepth=1,numsubs=1,useragent=UserAgent):
        self.markovdepth = markovdepth
        self.numsubs = numsubs
    def get_comments(self):
        reddit = praw.Reddit(user_agent=UserAgent)
        posts = reddit.get_subreddit('all').get_hot(limit=self.numsubs)
        self.comments = []
        for post in posts:
            post.replace_more_comments()
            comment_list = praw.helpers.flatten_tree(post.comments)
            post_comments = []
            post_sum = 0
            for comment in comment_list:
                post_comments.append(comment)
                post_sum += comment.score
            post_average = post_sum / len(comment_list)
            for comment in post_comments:
                if (comment.score > post_average):
                    self.comments.append(comment.body)

    def make_model(self):
        self.markovmodel = markovutils.MarkovModel([comment.split() for comment in self.comments],depth=self.markovdepth)

    def make_new_comment(self):
        return " ".join(self.markovmodel.generate())
