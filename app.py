from faceDetector import checkImage
from instaLoader import GetInstagramProfile
from fixLogin import updateSession
import os
from datetime import date

myface ="me.jpg"

# #for each picture in the folder downloads check if there is my face in it
# listOfFiles = []
# for filename in os.listdir("downloads"):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         if checkImage("downloads/"+filename,myface):
#             print("found my face in "+filename)
#             listOfFiles.append("downloads/"+filename)
#     else:
#         continue

# print("found in total "+str(len(listOfFiles))+" pictures with my face in it")
# print(listOfFiles)
def cleanConsole():
    #os.system('cls' if os.name=='nt' else 'clear')
    print("\n"*5)

def loadUsers(cls,fileName):
    with open(fileName) as f:
        content = f.readlines()
    flaggedUsers = [x.strip() for x in content]
    return flaggedUsers

def newUser(user,flaggedUsers):
    for u in flaggedUsers:
        if user.split("   ")[0] ==user:
            return False
    return True

def getDateFromUser(user,flaggedUsers):
    for u in flaggedUsers:
        if user.split("   ")[0] ==user:
            return u.split("   ")[1]
    return ""

def updateWatchlist(cls):
    #load watchlist in a list
    flaggedUsers = loadUsers(cls,"watchlist.txt")

    print("Updating watchlist from instagram...")
    cls.get_users_followings(cls.currentAccount,"watchlist.txt")

    newFlaggedUsers = loadUsers(cls,"watchlist.txt")


    #for each flag user, if there is no date (split by "   ") add current date
    date ="" 
    with open("watchlist.txt", "w") as f:
        for user in newFlaggedUsers:
            print("user:"+user)
            if newUser(user,flaggedUsers):
                if(date==""):
                        date = input("We found new users, please enter a date (yyyy,mm,dd) to start checking from: ")
                toWrite = user+"   "+str(date)+"\n"
                print("writing: "+toWrite)
                f.write(toWrite)
            else:
                f.write(user+"   "+getDateFromUser(user,flaggedUsers)+"\n")
            

def searchFromInsta(cls):
    #open watchlist and store profile to check in a list
    print("Searching and analyzing...")

    with open("watchlist.txt") as f:
        content = f.readlines()
    flaggedUsers = [x.strip() for x in content]

    for userInfo in flaggedUsers:
        user,date = userInfo.split("   ")
        print("checking user: "+user, "since date: "+date)
        try:
            cls.download_post_since_date(user,date.split(","))
        except:
            print("error downloading posts for user: "+user)
        # #check if there is my face in the pictures
        # listOfFiles = []
        # for filename in os.listdir("downloads"):
        #     if filename.endswith(".jpg") or filename.endswith(".png"):
        #         if checkImage("downloads/"+filename,myface):
        #             print("found my face in "+filename)
        #             listOfFiles.append("downloads/"+filename)
        #     else:
        #         continue
        # print("found in total "+str(len(listOfFiles))+" pictures with my face in it")
        # print(listOfFiles)

def deleteUselessFiles(whitelist):
    print("deleting files not flagged...")
    print("whitelist",whitelist)
    for filename in os.listdir("downloads"):
        if filename not in whitelist:
            #print("deleting "+filename)
            os.remove("downloads/"+filename)


def analyze():
    #check if there is my face in the pictures
    listOfFiles = []
    for filename in os.listdir("downloads"):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            if checkImage("downloads/"+filename,myface):
                print("found my face in "+filename)
                listOfFiles.append(filename)
        else:
            continue
    print("found in total "+str(len(listOfFiles))+" pictures with my face in it")
    return listOfFiles

def searchAndAnalyze(cls):
    print("----- Searching from instagram...")
    searchFromInsta(cls)
    print("----- Analyzing...")
    whitelist = analyze()
    print("----- Deleting useless files...")
    deleteUselessFiles(whitelist)

def displayMenu():
    print("1. Login")
    print("2. Update watchlist")
    print("3. Search and analyze")
    print("4. Exit")

def login(cls):
    account = updateSession() #input("Enter your account name: ")
    cls.loginFromSession(account)


cls = GetInstagramProfile()
exitApp = False
login(cls)
while (not exitApp):
    displayMenu()
    choice = input("Enter your choice: ")
    if choice == "1":
        login(cls)
    elif choice == "2":
        updateWatchlist(cls)
    elif choice == "3":
        searchAndAnalyze(cls)
    elif choice == "4":
        exitApp = True
    

# #try on accountWithPostOnMe
# cls.download_post_since_date("accountWithPostOnMe",[2022, 9, 1])