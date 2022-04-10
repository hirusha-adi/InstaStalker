import os
import json
import sys
from instaloader import Instaloader, Profile


class InstaProfile:
    def __init__(self, target: str = None):
        self.CLEAR = ("clear" if os.name == "posix" else "cls")
        self.TARGET = target

        self.insta = Instaloader()

        self.profile = None
        self.profile_dict = None
        self.uploaded_posts = None
        self.followers = None
        self.followees = None

    def ask(self, q: str):
        return input(q)

    def setTARGET(self, target):
        self.TARGET = target

    def login(self, username: str, password: str):
        self.insta.login(user=username, passwd=password)

    def processProfile(self):
        self.profile = Profile.from_username(self.insta.context, self.TARGET)
        self.profile_dict = {
            'username': self.profile.username,
            'profile_id': self.profile.userid,
            'is_private': self.profile.is_private,
            'followed_by_viewer': self.profile.followed_by_viewer,
            'mediacount': self.profile.mediacount,
            'igtv_count': self.profile.igtvcount,
            'followers': self.profile.followers,
            'followees': self.profile.followees,
            'external_url': self.profile.external_url,
            'is_business_account': self.profile.is_business_account,
            'business_category_name': self.profile.business_category_name,
            'biography': self.profile.biography,
            'blocked_by_viewer': self.profile.blocked_by_viewer,
            'follows_viewer': self.profile.follows_viewer,
            'full_name': self.profile.full_name,
            'has_blocked_viewer': self.profile.has_blocked_viewer,
            'has_highlight_reels': self.profile.has_highlight_reels,
            'has_public_story': self.profile.has_public_story,
            'has_viewable_story': self.profile.has_viewable_story,
            'has_requested_viewer': self.profile.has_requested_viewer,
            'is_verified': self.profile.is_verified,
            'requested_by_viewer': self.profile.requested_by_viewer,
            'profile_pic_url': self.profile.profile_pic_url
        }

    def getProfileInfo(self):
        if self.profile_dict is None:
            self.processProfile()
        return self.profile_dict

    def getPosts(self):
        if self.uploaded_posts is None:
            self.uploaded_posts = self.profile.get_posts()
        return self.uploaded_posts

    def savePosts(self):
        for post in self.getPosts():
            self.insta.download_post(
                post,
                target=self.profile.username
            )

    def getAllTaggedPosts(self):
        if self.tagged_posts is None:
            self.tagged_posts = self.profile.get_tagged_posts()
        return self.tagged_posts

    def saveAllTaggedPosts(self):
        for post in self.getAllTaggedPosts():
            self.insta.download_post(
                post,
                target=self.profile.username
            )

    def getAllIGTVPosts(self):
        if self.igtv_posts is None:
            self.igtv_posts = self.profile.get_igtv_posts()
        return self.igtv_posts

    def saveAllIGTVPosts(self):
        for post in self.getAllIGTVPosts():
            self.insta.download_post(
                post,
                target=self.profile.username
            )

    def saveAllPosts(self):
        self.savePosts()
        self.saveAllTaggedPosts()
        self.saveAllIGTVPosts()

    def getFollowersList(self):
        if self.followers is None:
            self.followers = self.profile.get_followers()
        return self.followers

    def saveFollowers(self, formatting: str = None, mode: str = "simple", output: str = "print_only"):
        """
        `formatting`: str -->
            count
            username
            full_name
            userid
            is_private
            is_verified
            meida_count
            followers
            followees
            is_business_account
            biography
            profile_pic_url
        
        `mode`: str -->
            low
            mid
            all/high

        `output`: str -->
            print_only
            json
            text
        """

        if formatting is None:
            if mode == "low":
                information = "{count} | {username} | {full_name}"
            elif mode == "mid":
                information = "{count} | {username} | {full_name} | {userid} | {is_private} | {is_verified} | {meida_count} | {followers} | {followees}"
            elif mode == "all" or mode == "high":
                information = "{count} | {username} | {full_name} | {userid} | {is_private} | {is_verified} | {meida_count} | {is_business_account} | {followers} | {followees} | {biography} | {profile_pic_url}"
        else:
            information = formatting

        followers = self.getFollowersList()

        if output == "print_only":
            count = 1
            for profile in followers:
                text = information.format(
                    count=count,
                    username=profile.username,
                    full_name=profile.full_name,
                    userid=profile.userid,
                    is_private=profile.is_private,
                    is_verified=profile.is_verified,
                    is_business_account=profile.is_business_account,
                    meida_count=profile.mediacount,
                    followers=profile.followers,
                    followees=profile.followees,
                    biography=profile.biography,
                    profile_pic_url=profile.profile_pic_url
                )                
                print(text)
                count += 1
        
        if output == "json":
            full_dict = {"data": []}
            count = 1
            for profile in followers:
                text = information.format(
                    count=count,
                    username=profile.username,
                    full_name=profile.full_name,
                    userid=profile.userid,
                    is_private=profile.is_private,
                    is_verified=profile.is_verified,
                    is_business_account=profile.is_business_account,
                    meida_count=profile.mediacount,
                    followers=profile.followers,
                    followees=profile.followees,
                    biography=profile.biography,
                    profile_pic_url=profile.profile_pic_url
                )                
                print(text)
                full_dict["data"].append(text)
                count += 1
            with open(os.path.join(os.getcwd(), str(self.profile.username) + "_followers.json"), "w", encoding="utf-8") as _file_followers:
                json.dump(full_dict, _file_followers)

        if output == "text":
            with open(os.path.join(os.getcwd(), str(self.profile.username) + "_followers.txt"), "w", encoding="utf-8") as _file_followers:
                count = 1
                for profile in followers:
                    text = information.format(
                        count=count,
                        username=profile.username,
                        full_name=profile.full_name,
                        userid=profile.userid,
                        is_private=profile.is_private,
                        is_verified=profile.is_verified,
                        is_business_account=profile.is_business_account,
                        meida_count=profile.mediacount,
                        followers=profile.followers,
                        followees=profile.followees,
                        biography=profile.biography,
                        profile_pic_url=profile.profile_pic_url
                    )                
                    print(text)
                    _file_followers.write(text + "\n")
                    count += 1

    def getFolloweesList(self):
        if self.followees:
            self.followees = self.profile.get_followees()
        return self.followees

    def saveFollowees(self, formatting: str = None, mode: str = "simple", output: str = "print_only"):
        """
        `formatting`: str -->
            count
            username
            full_name
            userid
            is_private
            is_verified
            meida_count
            followers
            followees
            is_business_account
            biography
            profile_pic_url
        
        `mode`: str -->
            low
            mid
            all/high
        
        `output`: str -->
            print_only
            json
            text
        """

        if formatting is None:
            if mode == "low":
                information = "{count} | {username} | {full_name}"
            elif mode == "mid":
                information = "{count} | {username} | {full_name} | {userid} | {is_private} | {is_verified} | {meida_count} | {followers} | {followees}"
            elif mode == "all" or mode == "high":
                information = "{count} | {username} | {full_name} | {userid} | {is_private} | {is_verified} | {meida_count} | {is_business_account} | {followers} | {followees} | {biography} | {profile_pic_url}"
        else:
            information = formatting

        followees = self.getFolloweesList()

        if output == "print_only":
            count = 1
            for profile in followees:
                text = information.format(
                    count=count,
                    username=profile.username,
                    full_name=profile.full_name,
                    userid=profile.userid,
                    is_private=profile.is_private,
                    is_verified=profile.is_verified,
                    is_business_account=profile.is_business_account,
                    meida_count=profile.mediacount,
                    followers=profile.followers,
                    followees=profile.followees,
                    biography=profile.biography,
                    profile_pic_url=profile.profile_pic_url
                )                
                print(text)
                count += 1
        
        if output == "json":
            full_dict = {"data": []}
            count = 1
            for profile in followees:
                text = information.format(
                    count=count,
                    username=profile.username,
                    full_name=profile.full_name,
                    userid=profile.userid,
                    is_private=profile.is_private,
                    is_verified=profile.is_verified,
                    is_business_account=profile.is_business_account,
                    meida_count=profile.mediacount,
                    followers=profile.followers,
                    followees=profile.followees,
                    biography=profile.biography,
                    profile_pic_url=profile.profile_pic_url
                )                
                print(text)
                full_dict["data"].append(text)
                count += 1
            with open(os.path.join(os.getcwd(), str(self.profile.username) + "_followees.json"), "w", encoding="utf-8") as _file_followees:
                json.dump(full_dict, _file_followees)


        if output == "text":
            with open(os.path.join(os.getcwd(), str(self.profile.username) + "_followees.txt"), "w", encoding="utf-8") as _file_followees:
                count = 1
                for profile in followees:
                    text = information.format(
                        count=count,
                        username=profile.username,
                        full_name=profile.full_name,
                        userid=profile.userid,
                        is_private=profile.is_private,
                        is_verified=profile.is_verified,
                        is_business_account=profile.is_business_account,
                        meida_count=profile.mediacount,
                        followers=profile.followers,
                        followees=profile.followees,
                        biography=profile.biography,
                        profile_pic_url=profile.profile_pic_url
                    )  
                    print(text)
                    _file_followees.write(text + "\n")
                    count += 1

    def saveProfileInfo(self):
        data = self.getProfileInfo()
        with open(os.path.join(os.getcwd(), str(self.profile.username) + ".json"), "w", encoding="utf-8") as file:
            json.dump(data, file)

    def saveAll(self):
        self.saveAllPosts()
        self.saveProfileInfo()
        self.saveFollowers()
        self.saveFollowees()


class Database:
    config_filename = os.path.join(os.getcwd(), "config.json")

    if not(os.path.isfile(config_filename)):
        with open(config_filename, "w", encoding="utf-8") as _file:
            _file.write(
                '{\n\t"username": "",\n\t"password": ""\n\t"web": {\n\t\t"host": "0.0.0.0",\n\t\t"port": 8080,\n\t\t"debug": false\n\t}\n}')

    with open(config_filename, "r", encoding="utf-8") as _file:
        _data = json.load(_file)

    USERNAME = _data["username"].strip()
    PASSWORD = _data["password"].strip()
        
    if USERNAME is None:
        username_file = os.path.join(os.getcwd(), "username.txt")
        if os.path.isfile(username_file):
            with open(username_file, "r", encoding="utf-8") as _uname_file:
                USERNAME = _uname_file.read().strip()
        else:
            sys.exit(
                "No username/email/phone-number is given to log-in. Please fill it in the `config.json` file or have it in the './username.txt' file")

    if PASSWORD is None:
        password_file = os.path.join(os.getcwd(), "password.txt")
        if os.path.isfile(password_file):
            with open(password_file, "r", encoding="utf-8") as _passwd_file:
                PASSWORD = _uname_file.read().strip()
        else:
            sys.exit(
                "No passowrd is given to log-in. Please fill it in the `config.json` file or have it in the './password.txt' file.")

    HOST = _data["web"]["host"]
    PORT = _data["web"]["port"]
    DEBUG = _data["web"]["debug"]