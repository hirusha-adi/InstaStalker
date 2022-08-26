import texts
import json
import os
import sys
from utils import pip_install

try:
    from instaloader import Instaloader, Profile
except:
    pip_install("instaloader")
    from instaloader import Instaloader, Profile
finally:
    from instaloader import Instaloader, Profile

class InstaProfile:
    def __init__(self, target: str = None):
        self.CLEAR = ("clear" if os.name == "posix" else "cls")
        self._TARGET = target

        self._insta = Instaloader(
            download_geotags=True,
            download_comments=True,
        )

        # variables used to store stuff of the user
        self._profile = None
        self._profile_data = None
        self._uploaded_posts = None
        self._tagged_posts = None
        self._igtv_posts = None
        self._followers = None
        self._followees = None
        self._followers_list = {'data': []}
        self._followees_list = {'data': []}

        # variables used to manage stuff of the object
        self._is_logged_in = False
        self._is_target_set = False
        self._is_profile_processed = False
        self._is_profile_set = False

    @property
    def TARGET(self): return self._TARGET

    @TARGET.setter
    def TARGET(self, target: str):
        if self._is_target_set:
            return False

        self._TARGET = target

        # Processing te profile once the target is set
        self._profile = Profile.from_username(
            self._insta.context,
            self._TARGET
        )
        self._is_profile_set = True

        self._is_target_set = True
        return True

    @property
    def insta(self): return self._insta

    @property
    def profile_data(self):
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
        if (self._profile_data is None) or (self._is_profile_processed is False):
            self._process_profile_data()
        return self._profile_data

    @profile_data.setter
    def profile_data(self, data: dict):
        self._profile_data = data

        if not self._is_profile_set:
            self._profile = Profile.from_username(
                self._insta.context,
                self._profile_data['username']
            )

        self._is_profile_processed = True

    @property
    def uploaded_posts(self):
        if self._uploaded_posts is None:
            self._process_PostsUploaded()
        return self._uploaded_posts  # NodeIterator[Post]

    @property
    def tagged_posts(self):
        if self._tagged_posts is None:
            self._process_PostsTagged()
        return self._tagged_posts  # NodeIterator[Post]

    @property
    def igtv_posts(self):
        if self._igtv_posts is None:
            self._process_PostsIGTV()
        return self._igtv_posts  # NodeIterator[Post]

    @property
    def followers(self):
        if self._followers is None:
            self._process_Followers()
        return self._followers  # NodeIterator[Profile]

    @property
    def followees(self):
        if self._followees is None:
            self._process_Followees()
        return self._followees  # NodeIterator[Profile]

    @property
    def followers_list(self): return self._followers_list

    @property
    def followees_list(self): return self._followees_list

    @property
    def is_logged_in(self): return self._is_logged_in

    @property
    def is_target_set(self): return self._is_target_set

    @property
    def is_profile_processed(self): return self._is_profile_processed

    @property
    def is_profile_set(self): return self._is_profile_set

    # Login into our instagram profile before scraping for data
    def login(self, username: str, password: str):
        if self._is_logged_in:
            return False

        self._insta.login(user=username, passwd=password)

        self._is_logged_in = True
        return True

    # Process the main profile data (and create a dict)
    def _process_profile_data(self):
        if self._is_profile_processed:
            return False
        else:
            if not self._is_profile_set:  # set the profile if has not been set in TARGET's setter
                self._profile = Profile.from_username(
                    self._insta.context, self._TARGET)
            self._profile_data = {
                'username': self._profile.username,
                'profile_id': self._profile.userid,
                'is_private': self._profile.is_private,
                'followed_by_viewer': self._profile.followed_by_viewer,
                'mediacount': self._profile.mediacount,
                'igtv_count': self._profile.igtvcount,
                'followers': self._profile.followers,
                'followees': self._profile.followees,
                'external_url': self._profile.external_url,
                'is_business_account': self._profile.is_business_account,
                'business_category_name': self._profile.business_category_name,
                'biography': self._profile.biography,
                'blocked_by_viewer': self._profile.blocked_by_viewer,
                'follows_viewer': self._profile.follows_viewer,
                'full_name': self._profile.full_name,
                'has_blocked_viewer': self._profile.has_blocked_viewer,
                'has_highlight_reels': self._profile.has_highlight_reels,
                'has_public_story': self._profile.has_public_story,
                'has_viewable_story': self._profile.has_viewable_story,
                'has_requested_viewer': self._profile.has_requested_viewer,
                'is_verified': self._profile.is_verified,
                'requested_by_viewer': self._profile.requested_by_viewer,
                'profile_pic_url': self._profile.profile_pic_url
            }
            self._is_profile_processed = True
            return True

    # process all uploaded posts
    def _process_PostsUploaded(self):
        if self._uploaded_posts is None:
            self._uploaded_posts = self._profile.get_posts()
        return self._uploaded_posts

    # Save all uploaded posts
    def save_PostsUploaded(self, home=None, save=None, subdir=False):

        # process uploaded posts list if not done before
        if self._uploaded_posts is None:
            self._process_PostsUploaded()

        if subdir:
            os.chdir(save)
            print("[+] Changed current working directory to", save)

        # iterate through all uploaded posts (NodeIterator[Post]) and save all
        count = 1
        for post in self._uploaded_posts:
            self._insta.download_post(
                post,
                target=str(count)
            )
            print(f"{count} - Saved Uploaded Post!")

        if subdir:
            os.chdir(home)
            print("[+] Changed current working directory back to", home)

        print(texts.COMPLETED)
        print("[+] SAVED ALL UPLOADED POSTS!")

    # process all tagged posts
    def _process_PostsTagged(self):
        if self._tagged_posts is None:
            self._tagged_posts = self._profile.get_tagged_posts()
        return self._tagged_posts

    # Save all tagged posts
    def save_PostsTagged(self, home=None, save=None, subdir=False):
        # process tagged posts list if not done before
        if self._tagged_posts is None:
            self._process_PostsTagged()

        if subdir:
            os.chdir(save)
            print("[+] Changed current working directory to", save)

        # iterate through all tagged posts (NodeIterator[Post]) and save all
        count = 1
        for post in self._tagged_posts:
            self._insta.download_post(
                post,
                target=str(count)
            )
            print(f"{count} - Saved Tagged Post!")

        if subdir:
            os.chdir(home)
            print("[+] Changed current working directory back to", home)

        print(texts.COMPLETED)
        print("[+] SAVED ALL UPLOADED POSTS!")

    # process all IGTV posts
    def _process_PostsIGTV(self):
        if self._igtv_posts is None:
            self._igtv_posts = self._profile.get_igtv_posts()
        return self._igtv_posts

    # Save all IGTV posts
    def save_PostsIGTV(self, home=None, save=None, subdir=False):
        # process IGTV posts list if not done before
        if self._igtv_posts is None:
            self._process_PostsIGTV()

        if subdir:
            os.chdir(save)
            print("[+] Changed current working directory to", save)

        # iterate through all IGTV posts (NodeIterator[Post]) and save all
        count = 1
        for post in self._igtv_posts:
            self._insta.download_post(
                post,
                target=str(count)
            )
            print(f"{count} - Saved IGTV Post!")

        if subdir:
            os.chdir(home)
            print("[+] Changed current working directory back to", home)

        print(texts.COMPLETED)
        print("[+] SAVED ALL UPLOADED POSTS!")

    # Use all the three functions together at once to save all posts -->
    # Uploaded Posts, Tagged Posts and IGTV Posts
    def save_PostsAll(self):
        self.save_PostsUploaded()
        self.save_PostsTagged()
        self.save_PostsIGTV()

    # process all followers list
    def _process_Followers(self):
        if self._followers is None:
            self._followers = self._profile.get_followers()
        return self._followers

    # process all followees list
    def _process_Followees(self):
        if self._followees:
            self._followees = self._profile.get_followees()
        return self._followees

    def save_FollowersFollowees(
        self,
        followers_or_followees: str,
        final_file_name=None,
        mode: str = "simple",
        output: str = "json",
        formatting: str = None,
        save_path=None,
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
            all/high (default)

        `output`: str -->
            print_only
            text

        `save_path`: str -->
            Folder/Directory Path
        """

        # Prioritize Custom Formatting
        if formatting is None:
            # Default to a mode if custom formatting is not specified
            if mode == "low":
                information = "{count} | {username} | {full_name}"
            elif mode == "mid":
                information = "{count} | {username} | {full_name} | {userid} | {is_private} | {is_verified} | {meida_count} | {followers} | {followees}"
            else:
                information = "{count} | {username} | {full_name} | {userid} | {is_private} | {is_verified} | {meida_count} | {is_business_account} | {followers} | {followees} | {biography} | {profile_pic_url}"
        else:
            # Query String equals to custom formatting provided
            information = formatting

        # Decide weather to get followers or followees
        if followers_or_followees.lower().strip() == "followers":
            users_list = self._process_Followers()
            followers = True
        elif followers_or_followees.lower().strip() == "followees":
            users_list = self._process_Followees()
            followers = False
        else:
            # Exit program is wrong value is given, because this is essential
            sys.exit(
                'Error: Improper value for `followers_or_followees` has been passed to `saveFollowersFollowees()`')

        if final_file_name is None:

            # Save File Name
            if save_path is None:
                file_name = os.path.join(
                    os.getcwd(),
                    str(self._profile.username) +
                    f"_{'followers' if followers == True else 'followees'}"
                )

            # If save_path is a string
            if isinstance(save_path, str):
                # If save_path does not end with a .json or .txt, consider it as a folder
                if not(save_path.endswith(".json") or save_path.endswith(".txt")):
                    if not(os.path.isdir(save_path)):
                        # Create this directory if it does not exist
                        os.makedirs(save_path)
                    # make save file name from the save_path dir
                    file_name = os.path.join(
                        save_path,
                        f"{self._TARGET}_{'followers' if followers == True else 'followees'}"
                    )
                else:
                    # If save_path end with a .json or .txt, consider it as the file name
                    file_name = os.path.join(save_path)

        else:
            file_name = final_file_name

        # Add file extension if not in file_name
        if (output == "txt") or (output == "text"):
            if not file_name.lower().endswith(".txt"):
                file_name += ".txt"
            text_file = True
        else:
            # Default to json
            if not file_name.lower().endswith(".json"):
                file_name += ".json"
            text_file = False

        # Add the query format as the first element of the list
        if followers:
            self._followers_list['data'].append(information)
        else:
            self._followees_list['data'].append(information)

        print("\n[+] Selected Formatting for saving follower/followee information: ")
        print(information)

        with open(file_name, "w", encoding="utf-8") as _file_follow:

            count = 1  # keep track of the count

            # Iterate through the returned NodeIterator[Profile]
            for profile in users_list:

                # Format the query (set with a mode or custom formatting)
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

                # If Followers are selected
                if followers:
                    # Add this to the final dict
                    self._followers_list['data'].append(text)
                else:
                    self._followees_list['data'].append(text)

                # Display the current info
                print(text, "\n")

                # If txt file, write the line to the file
                if text_file:
                    _file_follow.write(text + "\n")

                # Increase the count
                count += 1

            # The for loop ends here ------

            # if not text_file, defaults to json from above-processed final dict
            if not text_file:
                # dump dicts to the file
                if self.followers:
                    json.dump(self._followers_list, _file_follow)
                else:
                    json.dump(self._followees_list, _file_follow)

        print(texts.COMPLETED)
        print(
            f"\n[+] Saved all {'followers' if followers == True else 'followees'} list to {file_name}")

    # Create text from a dictionary. returns `str`
    def format_ProfileInfo_Dict2TXT(self, data):
        return f"""Username: {data['username']}
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
\nBiography: \n{data['biography']}\n
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
Profile pic url: {data['profile_pic_url']}"""

    # Save profile info
    def save_ProfileInfo(self, file_format: str = "json", filename: str = None, save_path=None, final_filename=None):
        """
        Dump Base Profile Info

        Args:
            file_format (str, optional): `json` or `txt`. Defaults to "json"
            save_path (str, optional): dir path. Defaults to ./username/
            filename (str, optional): filename. Defaults to save_path/filename
            final_filename (str, optional): highest precedence. filename
        """
        if final_filename is None:
            if save_path is None:
                # Default to ./username/ dir
                save_path = os.path.join(
                    os.getcwd(),
                    self._TARGET
                )

            # create base save folder if not exist
            if not os.path.isdir(save_path):
                os.makedirs(save_path)

            if filename is None:
                # default to target username
                filename_file = os.path.join(
                    save_path,
                    str(self._TARGET)
                )

                if file_format == "txt":
                    if not(filename_file.endswith(".txt")):
                        filename_file += ".txt"
                else:
                    if not(filename_file.endswith(".json")):
                        filename_file += ".json"

            else:
                if file_format == "txt":
                    if not(filename.endswith(".txt")):
                        filename += ".txt"
                else:
                    if not(filename.endswith(".json")):
                        filename += ".json"

                filename_file = os.path.join(save_path, filename)
        else:
            filename_file = final_filename

        if self._profile_data is None:
            self._process_profile_data()

        data = self._profile_data

        # Write data to file based on its format
        with open(filename_file, "w", encoding="utf-8") as file:
            if file_format == "txt":
                file.write(self.format_ProfileInfo_Dict2TXT(data=data))
            else:
                json.dump(data, file, ensure_ascii=True, indent=4)

    def save_Everything(self, level: str = "low"):
        """
        Dump/Save all information of the target instagram profile

        Args:
            level (str, optional): `all`/`high`, `mid`, `low` are the only possible values. Defaults to "high".
        """
        if not level in ("all", "mid", "low", "high"):
            level = "high"

        self.save_ProfileInfo(file_format="json")
        self.save_PostsAll()

        self.save_FollowersFollowees(
            followers_or_followees="followers",
            formatting=None,
            mode=level,
            output="json"
        )
        self.save_FollowersFollowees(
            followers_or_followees="followees",
            formatting=None,
            mode=level,
            output="json"
        )
