from manager import InstaProfile, Database
import os, sys


obj = InstaProfile()
obj.setTARGET("ac3.desu")
obj.login(username=Database.USERNAME, password=Database.PASSWORD)


accinfo = obj.getProfileInfo()

