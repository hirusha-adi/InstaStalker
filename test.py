from instaloader import Instaloader, Profile
import os

TARGET = "Any-Username"

# Create object
insta = Instaloader()

# Login
insta.login(user="username", passwd="password")

# Set Username
profile = Profile.from_username(
    insta.context,
    TARGET
)

# Get Posts
uploaded_posts = profile.get_posts()

# custom save folder
save_folder = os.path.join(
    os.getcwd(),
    "static",
    "data",
    TARGET,
    "posts",
    "uploaded"
)
if not(os.path.isdir(save_folder)):
    os.makedirs(save_folder)

# Start Saving posts with a count
count = 1
for post in uploaded_posts:
    print(count)
    # print(
    # f"[{count}]: Title: {post.title}\n\tCaption: {post.caption}\n\tDate: {post.date}\n\tURL:{post.url}\n")
    insta.download_post(
        post,
        target=save_folder
    )
