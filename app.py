from faceDetector import checkImage
from instaLoader import GetInstagramProfile
from fixLogin import updateSession
import os
from datetime import date as dt

#get date in format yyyy,mm,dd
def getTodayDate():
    today = dt.today()
    return str(today.year)+","+str(today.month)+","+str(today.day)

def cleanConsole():
    #os.system('cls' if os.name=='nt' else 'clear')
    print("\n"*5)

def loadUsers(cls,fileName):
    with open(fileName) as f:
        content = f.readlines()
    flaggedUsers = [x.strip() for x in content]
    return flaggedUsers

def newUser(user,users):
    similarUsers =0
    for u in users:
        if u.split("   ")[0] ==user:
            similarUsers+=1
    return similarUsers==0

def getDateFromUser(user,flaggedUsers):
    for u in flaggedUsers:
        if user.split("   ")[0] ==user:
            return u.split("   ")[1]
    return ""

def updateWatchlist(cls):
    #load watchlist in a list
    print("Loading watchlist...")
    flaggedUsers = loadUsers(cls,"watchlist.txt")
    print("total users in watchlist: "+str(len(flaggedUsers)))

    print("fetching updated followers from instagram...")
    cls.get_users_followings(cls.currentAccount,"watchlist.txt")
    newFlaggedUsers = loadUsers(cls,"watchlist.txt")

    #for each flag user, if there is no date (split by "   ") add current date
    date ="" 
    with open("watchlist.txt", "w") as f:
        for user in newFlaggedUsers:
            #print("user:"+user)
            if newUser(user,flaggedUsers):
                print("found new user: "+user)
                if(date==""):
                        date = input("We found new users, please enter a date (yyyy,mm,dd) to start checking from: ")
                toWrite = user+"   "+str(date)+"\n"
                #print("writing: "+toWrite)
                f.write(toWrite)
            else:
                #print("existing user: "+user)
                f.write(user+"   "+getDateFromUser(user,flaggedUsers)+"\n")
            

def searchFromInsta(cls):
    #open watchlist and store profile to check in a list
    print("Searching and analyzing...")

    with open("watchlist.txt") as f:
        content = f.readlines()
    flaggedUsers = [x.strip() for x in content]
    flaggedUsersChecked = []
    i=1
    nUsers = len(flaggedUsers)
    for userInfo in flaggedUsers:
        user,date = userInfo.split("   ")
        print(f"[{i}/{nUsers}] checking user: {user} since date: {date}")
        try:
            cls.download_post_since_date(user,date.split(","))
            flaggedUsersChecked.append(user)
        except:
            print("error downloading posts for user: "+user)
        i+=1
    
    #update watchlist date for today for all users checked
    with open("watchlist.txt", "w") as f:
        for user in flaggedUsers:
            if user.split("   ")[0] in flaggedUsersChecked:
                f.write(user.split("   ")[0]+"   "+getTodayDate()+"\n")
            else:
                f.write(user+"\n")


def deleteUselessFiles(whitelist):
    print("deleting files not flagged and empty folders...")
    print("files flagged: ",whitelist)

    #list all folder in downloads
    for folder in os.listdir("downloads"):
        for filename in os.listdir("downloads/"+folder):
            if filename not in whitelist:
                #print("deleting "+filename)
                os.remove("downloads/"+folder+"/"+filename)
        #if folder is empty, delete it
        if len(os.listdir("downloads/"+folder))==0:
            os.rmdir("downloads/"+folder)


def analyze():
    #check if there is my face in the pictures
    listOfFiles = []
    listOfUsersFlagged=[]
    for folder in os.listdir("downloads"):
        for filename in os.listdir("downloads/"+folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                if checkImage("downloads/"+folder+"/"+filename,myface):
                    print("found my face in "+filename)
                    listOfFiles.append(filename)
                    if folder not in listOfUsersFlagged:
                        listOfUsersFlagged.append(folder)
            else:
                continue
    print("found in total "+str(len(listOfFiles))+" pictures with my face in it")
    return listOfFiles,listOfUsersFlagged

def analyzeFlagAndClean():
    print("----- Analyzing...")
    whitelist,usersFlagged = analyze()
    print("----- Deleting useless files...")
    deleteUselessFiles(whitelist)

    print("----- Flagged users:")
    with open("flaggedUsers.txt", "w") as f:
        for user in usersFlagged:
            f.write(user+"\n")
            print(user)
    print("exported in flaggedUsers.txt")


def searchAndAnalyze(cls):
    print("----- Searching from instagram...")
    searchFromInsta(cls)
    analyzeFlagAndClean()


def displayMenu():
    print("1. Login")
    print("2. Update watchlist")
    print("3. Search and analyze")
    print("4. Search only")
    print("5. Analyze only")
    print("9. Exit")

def login(cls):
    account = updateSession()
    cls.loginFromSession(account)


cls = GetInstagramProfile()
exitApp = False
login(cls)
myface ="me.jpg"
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
        searchFromInsta(cls)
    elif choice == "5":
        analyzeFlagAndClean()
    elif choice == "9":
        exitApp = True
    

# #try on accountWithPostOnMe
# cls.download_post_since_date("accountWithPostOnMe",[2022, 9, 1])