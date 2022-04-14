#!/usr/bin/python3

import instaloader
import sys


def show_help():
    print("""
      (: Instagram Profile Stalker v1.0 by ZeaCeR#5641 :)

         igpfp <username> [mode=pfp] [uname] [passwd]

Example -->
    igpfp hirushadi pfp

Values for: [mode] -->
    pfp      |  (default) Download only the profile picture
    stories  |  Download only stories
    tagged   |  Download only tagged images
    all      |  Download all

[uname] and [passwd] should be given only if you want to login,
If not given, will try to scrap without loggin in! ~ Errornous
          """)


root = instaloader.Instaloader()

args = sys.argv[:]

try:
    username = args[1]
except IndexError:
    show_help()
    sys.exit()

try:
    mode = args[2]
    if not(mode in ("stories", "pfp", "tagged", "all", "profilepic")):
        mode = "pfp"
        print("No [mode] is specified, defaulting to `pfp` (profile picture only)")
except IndexError:
    print("No [mode] is specified, defaulting to `pfp` (profile picture only)")
    mode = "pfp"

logininsta = True
try:
    uname = args[3]
    try:
        passwd = args[3]
    except IndexError:
        print("No [passwd] / Password is given to log in. Trying without logging in")
        logininsta = False
except IndexError:
    print("No [uname] / Username is given to log in. Trying without logging in")
    logininsta = False

if logininsta:
    root.login(user=uname, passwd=passwd)

if mode == "stories":
    print(root.download_profile(
        username,
        download_stories_only=True
    ))
    sys.exit("DONE!")

elif mode == "tagged":
    print(root.download_profile(
        username,
        download_tagged_only=True
    ))
    sys.exit("DONE!")

elif mode == "all":
    print(
        root.download_profile(
            username,
            profile_pic=True,
            download_stories=True,
            download_tagged=True
        )
    )
    sys.exit("DONE!")

else:
    print(root.download_profile(
        username,
        profile_pic_only=True
    ))
    sys.exit("DONE!")
