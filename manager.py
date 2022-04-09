import os
from instaloader import Instaloader, Profile


class Manager:
    def __init__(self, target: str = None):
        self.CLEAR = ("clear" if os.name == "posix" else "cls")
        self.TARGET = target

        self.insta = Instaloader()

        self.profile = None
        self.profile_dict = None

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
        return self.profile_dict
