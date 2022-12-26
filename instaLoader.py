import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile
import csv

class GetInstagramProfile():
    def __init__(self) -> None:
        self.L = instaloader.Instaloader()
        self.currentAccount = ""

    def loginFromSession(self,sessionName):
        self.L.load_session_from_file(sessionName)
        self.currentAccount = sessionName

    def download_users_profile_picture(self,username):
        self.L.download_profile(username, profile_pic_only=True)

    def download_users_posts_with_periods(self,username):
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        SINCE = datetime(2021, 8, 28)
        UNTIL = datetime(2021, 9, 30)

        for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
            self.L.download_post(post, username)

    def download_hastag_posts(self, hashtag):
        for post in instaloader.Hashtag.from_name(self.L.context, hashtag).get_posts():
            self.L.download_post(post, target='#'+hashtag)

    def get_users_followers(self,user_name):
        global user,pwd
        '''Note: login required to get a profile's followers.'''
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        print(profile.followers, "followers")

        print("{} follows these profiles:".format(profile.username))
        for followee in profile.get_followers():
            print("fol:",followee.username)

    def get_users_followings(self,user_name,outputfile):
        '''Note: login required to get a profile's followings.'''
        #self.L.login(input("input your username: "), input("input your password: ") ) 
        profile = instaloader.Profile.from_username(self.L.context, user_name)
        file = open(outputfile,"w")
        for followee in profile.get_followers():
            username = followee.username
            file.write(username + "\n")
            print(username)
        file.close()

    def get_post_comments(self,username):
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        for post in posts:
            for comment in post.get_comments():
                print("comment.id  : "+str(comment.id))
                print("comment.owner.username  : "+comment.owner.username)
                print("comment.text  : "+comment.text)
                print("comment.created_at_utc  : "+str(comment.created_at_utc))
                print("************************************************")

    def get_post_info_csv(self,username):
        with open(username+'.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
            for post in posts:
                print("post date: "+str(post.date))
                print("post profile: "+post.profile)
                print("post caption: "+post.caption)
                print("post location: "+str(post.location))
                
                posturl = "https://www.instagram.com/p/"+post.shortcode
                print("post url: "+posturl)
                writer.writerow(["post",post.mediaid, post.profile, post.caption, post.date, post.location, posturl,  post.typename, post.mediacount, post.caption_hashtags, post.caption_mentions, post.tagged_users, post.likes, post.comments,  post.title,  post.url ])
            
                for comment in post.get_comments():
                    writer.writerow(["comment",comment.id, comment.owner.username,comment.text,comment.created_at_utc])
                    print("comment username: "+comment.owner.username)
                    print("comment text: "+comment.text)
                    print("comment date : "+str(comment.created_at_utc))
                print("\n\n")

    def download_post_since_date(self,username,date):
        posts = instaloader.Profile.from_username(self.L.context, username).get_posts()
        SINCE = datetime(int(date[0]), int(date[1]), int(date[2]))
        #until now
        UNTIL = datetime.now()

        for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
            self.L.download_post(post, "downloads")

