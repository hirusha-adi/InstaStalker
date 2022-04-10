from manager import InstaProfile, Database
import os
import sys


obj = InstaProfile()
obj.setTARGET("ac3.desu")
obj.login(username=Database.USERNAME, password=Database.PASSWORD)


accinfo = obj.getProfileInfo()

CLEAR = 'clear' if os.name == 'posix' else 'cls'


def show_logo():
    print(r"""
    ____           __        _____ __        ____            
   /  _/___  _____/ /_____ _/ ___// /_____ _/ / /_____  _____
   / // __ \/ ___/ __/ __ `/\__ \/ __/ __ `/ / //_/ _ \/ ___/
 _/ // / / (__  ) /_/ /_/ /___/ / /_/ /_/ / / ,< /  __/ /    
/___/_/ /_/____/\__/\__,_//____/\__/\__,_/_/_/|_|\___/_/     
                        
                           v1.0
                    Made by ZeaCeR#5641                                     
    """)


def show_logo_profile():
    print(r"""
            ____             _____ __   
           / __ \_________  / __(_) /__ 
          / /_/ / ___/ __ \/ /_/ / / _ \
         / ____/ /  / /_/ / __/ / /  __/
        /_/   /_/   \____/_/ /_/_/\___/ 

    """)


def show_help_main_menu():
    print(r"""
Available commands in the home menu,
    [1] help --> display this text

    [2] target --> set target if not set
    [3] login --> login to instagram account

    [4] profile --> profile menu
    [5] posts --> posts menu
    [6] followers --> followers menu 
    [7] followees --> followees menu
    [8] DUMP ALL (BETA)
    
    [9] clear --> Clear Screen/Console
    [10] exit --> exit the script 
    """)


def show_help_profile_menu():
    print(r"""
Available commands in the home menu,
    [1] help --> display this text

    []
    """)


def clear_screen():
    os.system(CLEAR)


def ENTIRE_PROGRAM():
    show_logo()

    # Main Menu Option
    mmo = input("home> ").strip()

    if (mmo == 'help') or (mmo == '1'):
        show_help_main_menu()
        input("Press `Enter` to go back!")
        ENTIRE_PROGRAM()

    elif (mmo == 'target') or (mmo == '2'):
        target_username = input("target's username> ").strip()
        target = insta.setTARGET(target=target_username)
        if target:
            print("[+] Target username has been set!")
        else:
            print("[-] Skipping! Target username has been set already!")
        ENTIRE_PROGRAM()

    elif (mmo == 'login') or (mmo == '3'):
        login_username = input("username> ")
        login_password = input("password> ")
        print("[*] Please wait user is logging in!")
        login_status = insta.login(
            username=login_username,
            password=login_password
        )
        if login_status:
            print("[+] Logged in successfully!")
        else:
            print("[+] Skipping! User is already logged in!")
        ENTIRE_PROGRAM()

    elif (mmo == 'profile') or (mmo == '4'):
        show_logo_profile()

        print('[*] Please wait while information is being gathered!')
        profile_info = insta.getProfileInfo()
        print('[+] Done!')

        mm1 = input('profile> ').strip()
        if (mm1 == 'help') or (mm1 == '1'):
            show_help_profile_menu()
            input("Press `Enter` to go back!")
            ENTIRE_PROGRAM()


if __name__ == "__main__":
    print('[*] Please wait while the object is being instantiated!')
    insta = InstaProfile()
    print('[+] Done!')
    clear_screen()
    ENTIRE_PROGRAM()
