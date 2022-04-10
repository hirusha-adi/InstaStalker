from instaloader import Instaloader, Profile

ig = Instaloader()

# ig.login("", "")        # (login)

USERNAME = "hirushaadi"
profile = Profile.from_username(ig.context, USERNAME)


# print("{} follows these profiles:".format(profile.username))
# for followee in profile.get_followees():
#     print(followee.username)

print(f'''
Username: {profile.username}
Profile ID: {profile.userid}
Is private?: {profile.is_private}
Followed by viewer: {profile.followed_by_viewer}
Media Count: {profile.mediacount}
IGTV Count: {profile.igtvcount}
Followers: {profile.followers}
Followees: {profile.followees}
External URL: {profile.external_url}
Is Bussiness Account: {profile.is_business_account}
Bussiness Category Name: {profile.business_category_name}
Biography: {profile.biography}
Blocked by viewer: {profile.blocked_by_viewer}
Follows Viewer: {profile.follows_viewer}
Full Name: {profile.full_name}
Has blocked viewer: {profile.has_blocked_viewer}
Has Highlight reels: {profile.has_highlight_reels}
Has public story: {profile.has_public_story}
Has viewable story: {profile.has_viewable_story}
Has requested Viewer: {profile.has_requested_viewer}
Is verified: {profile.is_verified}
Requested by Viewer: {profile.requested_by_viewer}
Profile Pic URL: {profile.profile_pic_url}
      ''')

# Retrieve all posts from a profile.
all_posts = profile.get_posts()  # returns NodeIterator[Post]
for post in all_posts:
    ig.download_post(post, target=profile.username)

# Retrieve all posts where a profile is tagged.
tagged_posts = profile.get_tagged_posts()  # returns NodeIterator[Post]

# Retrieve all IGTV posts.
igtv_posts = profile.get_igtv_posts()  # returns NodeIterator[Post]

# Retrieve list of followers of given profile. To use this, one needs to be logged in and private profiles has to be followed.
followers = profile.get_followers()  # returns NodeIterator[Profile]


# Retrieve list of followees (followings) of given profile. To use this, one needs to be logged in and private profiles has to be followed.
followees = profile.get_followees()  # returns NodeIterator[Profile]

# Retrieve list of suggested / similar accounts for this profile. To use this, one needs to be logged in.
similiar_accounts = profile.get_similar_accounts()  # returns Iterator[Profile]
