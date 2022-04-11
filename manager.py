import os
import json
import sys
from instaloader import Instaloader, Profile


class InstaProfile:
    def __init__(self, target: str = None):
        self.CLEAR = ("clear" if os.name == "posix" else "cls")
        self.TARGET = target

        self.insta = Instaloader()

        # variables used to store stuff of the user
        self.profile = None
        self.profile_dict = None
        self.uploaded_posts = None
        self.followers = None
        self.followees = None

        # variables used to manage stuff of the object
        self.is_logged_in = False
        self.is_target_set = False
        self.is_profile_processed = False

    def ask(self, q: str):
        """
        Take uer input
        """
        return input(q)

    def setTARGET(self, target: str):
        """
        Set the taget user

        Args:
            target (str): Target's username of the instagram account
        """
        if self.is_target_set:
            return False
        self.TARGET = target
        self.is_target_set = True
        return True

    def login(self, username: str, password: str):
        """
        Login into your instagram account

        Args:
            username (str): Username/Email/Phone-Number of the instagram account
            password (str): Password of the instagram account
        """
        if self.is_logged_in:
            return False
        self.insta.login(user=username, passwd=password)
        self.is_logged_in = True

    def processProfile(self):
        """
        Process the target profile's basic information
        """
        if self.is_profile_processed:
            return False
        else:
            self.is_profile_processed = True
            self.profile = Profile.from_username(
                self.insta.context, self.TARGET)
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
            return True

    def getProfileInfo(self):
        """
        Get the basic information of the target profile

        Returns:
            dict: with keys -->
                "username"
                "profile_id"
                "is_private"
                "followed_by_viewer"
                "mediacount"
                "igtv_count"
                "followers"
                "followees"
                "external_url"
                "is_business_account"
                "business_category_name"
                "biography"
                "blocked_by_viewer"
                "follows_viewer"
                "full_name"
                "has_blocked_viewer"
                "has_highlight_reels"
                "has_public_story"
                "has_viewable_story"
                "has_requested_viewer"
                "is_verified"
                "requested_by_viewer"
                "profile_pic_url"
        """
        if (self.profile_dict is None) or (self.is_profile_processed is False):
            self.processProfile()
        return self.profile_dict

    def getPosts(self):
        """
        get the Post list uploaded by the target user

        Returns:
            NodeIterator[Post]
        """
        if self.uploaded_posts is None:
            self.uploaded_posts = self.profile.get_posts()
        return self.uploaded_posts

    def savePosts(self):
        """
        Save all the posts uploaded by the target user
            insde `./targetUserName/` directory
        """
        for post in self.getPosts():
            self.insta.download_post(
                post,
                target=self.profile.username
            )

    def getAllTaggedPosts(self):
        """
        get all Posts that have tagged the target user

        Returns:
            NodeIterator[Post]
        """
        if self.tagged_posts is None:
            self.tagged_posts = self.profile.get_tagged_posts()
        return self.tagged_posts

    def saveAllTaggedPosts(self):
        """
        Save all Posts that have tagged the target user
            insde `./targetUserName/` directory
        """
        for post in self.getAllTaggedPosts():
            self.insta.download_post(
                post,
                target=self.profile.username
            )

    def getAllIGTVPosts(self):
        """
        get the IGTV list uploaded by the target user

        Returns:
            NodeIterator[Post]
        """
        if self.igtv_posts is None:
            self.igtv_posts = self.profile.get_igtv_posts()
        return self.igtv_posts

    def saveAllIGTVPosts(self):
        """
        Save all the IGTV uploaded by the target user
            insde `./targetUserName/` directory
        """
        for post in self.getAllIGTVPosts():
            self.insta.download_post(
                post,
                target=self.profile.username
            )

    def saveAllPosts(self):
        """
        Save all posts -->
            uploaded by the target +
            where the target has been tagged and
            in IGTV
        """
        self.savePosts()
        self.saveAllTaggedPosts()
        self.saveAllIGTVPosts()

    def getFollowersList(self):
        """
        get the follower list of the target

        Returns:
            NodeIterator[Profile]
        """
        if self.followers is None:
            self.followers = self.profile.get_followers()
        return self.followers

    def getFolloweesList(self):
        """
        get the followee list of the target

        Returns:
            NodeIterator[Profile]
        """
        if self.followees:
            self.followees = self.profile.get_followees()
        return self.followees

    def saveFollowersFollowees(
        self,
        followers_or_followees: str,
        formatting: str = None,
        mode: str = "simple",
        output: str = "text"
    ):
        """
        `followers_or_followees`: str -->
            followers
            followees

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

        if followers_or_followees.lower().strip() == "followers":
            users_list = self.getFollowersList()
            followers = True
        elif followers_or_followees.lower().strip() == "followees":
            users_list = self.getFolloweesList()
            followers = False
        else:
            sys.exit(
                'Error: Improper value for `followers_or_followees` has been passed to `saveFollowersFollowees()`')

        if output == "print_only":
            count = 1
            for profile in users_list:
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

        else:  # `text`
            with open(os.path.join(os.getcwd(), str(self.profile.username) + f"_{'followers' if followers == True else 'followees'}.txt"), "w", encoding="utf-8") as _file_follow:
                count = 1
                for profile in users_list:
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
                    _file_follow.write(text + "\n")
                    count += 1

    def saveProfileInfo(self, file_format: str = "json", filename: str = None):
        if filename is None:
            filename_file = os.path.join(
                os.getcwd(), str(self.profile.username) + ".json")
        else:
            if file_format == "txt":
                if not(filename.endswith(".txt")):
                    filename += ".txt"
            else:
                if not(filename.endswith(".json")):
                    filename += ".json"

            filename_file = os.path.join(os.getcwd(), filename)

        data = self.getProfileInfo()
        with open(filename_file, "w", encoding="utf-8") as file:
            if file_format == "txt":
                file.write(f"""
Username: {data['username']}
Profile ID: {data['profile_id']}
Is Private: {data['is_private']}
Followed by viewer: {data['followed_by_viewer']}
Media Count: {data['mediacount']}
IGTV Count: {data['igtv_count']}
Followers: {data['followers']}
Followees: {data['followees']}
External URL: {data['external_url']}
Is Business Account: {data['is_business_account']}
Business Category Name: {data['business_category_name']}
Bography: {data['biography']}
Blocked by viewer: {data['blocked_by_viewer']}
Follows viewer: {data['follows_viewer']}
Full Name: {data['full_name']}
Has blocked viewer: {data['has_blocked_viewer']}
Has highlight reels: {data['has_highlight_reels']}
Has public story: {data['has_public_story']}
Has viewable story: {data['has_viewable_story']}
Has requested viewer: {data['has_requested_viewer']}
Is Verified: {data['is_verified']}
Requested by viewer: {data['requested_by_viewer']}
Profile pic url: {data['profile_pic_url']}
                """)
            else:
                json.dump(data, file)

    def saveAll(self):
        self.saveProfileInfo()
        self.saveAllPosts()
        self.saveFollowersFollowees(followers_or_followees="followers")
        self.saveFollowersFollowees(followers_or_followees="followees")


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
