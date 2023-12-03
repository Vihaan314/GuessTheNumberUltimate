import random 
import time
from tkinter import *
import math
import os

print("Guess The Number")
time.sleep(0.5)

def finish():
    window.destroy()
    exit()
def saveScore(name, difficulty, numMax, randomChoice, attempts, tries):
    f = open("Guess_the_number_" + name + ".txt", "a")
    f.write("Name: " + name + "\nDifficulty: " + difficulty + "\nNumber range: 1 - " + str(numMax) + "\nNumber: " + str(randomChoice) + "\nAttempts: " + str(attempts) + "\nTries left: " + str(tries) + "\n")
    f.close()
def saveScoreLeaderboard(difficulty):
    f = open("Leaderboard_" + difficulty + ".txt", "a")
    if os.stat("Leaderboard_" + difficulty + ".txt").st_size == 0:
        f.write(difficulty.capitalize() + " leaderboard\n")
        f.write("\n".join("%s %s" % i for i in b))
        f.close()
    else:
        f.write("\n")
        f.write("\n".join("%s %s" % i for i in b))
        f.close()
        
def savePlaySingle(name, difficulty , numMax, randomChoice, attempts, tries):
    window = Tk()
    window.title("Save or Play again")
    window.geometry("100x75")
    window.configure(bg="Light blue")

    save = Button(window, text="Save score", bg="Yellow", command = lambda: saveScore(name, difficulty, numMax, randomChoice, attempts, tries)).pack()
    playAgain = Button(window, text="Play again", bg="Light green", command = runWithCount).pack()
    end = Button(window, text="End game", bg="Red", command = finish).pack()
    
def savePlayMulti(name, difficulty , numMax, randomChoice, attempts, tries):
    window = Tk()
    window.title("Save or Play again")
    window.geometry("100x75")
    window.configure(bg="Light blue")

    saveL = Button(window, text="Save leaderboard", bg="Yellow", command = lambda: saveScoreLeaderboard(difficulty)).pack()
    playAgain = Button(window, text="Play again", bg="Light green", command = multi).pack()
    end = Button(window, text="End game", bg="Red", command = finish).pack()


def setupGame():
    global difficulty
    global numMax
    global number
    
    difficulty = input("Choose difficulty - [Easy / Medium / Hard / Default]: ")
    while difficulty.lower() not in ["easy", "medium", "hard", "default"]:
        difficulty = input("Choose difficulty - [Easy / Medium / Hard / Default]: ")
    if difficulty.lower() == "easy":
        numMax = 10
    elif difficulty.lower() == "medium":
        numMax = 100
    elif difficulty.lower() == "hard":
        numMax = 500
    else:
        numMax = 100
    number = input("Choose the number generation range ({} or greater): 1 and... ".format(numMax))
    
    while number.isdigit() == False:
        print("Please enter a valid number!")
        number = input("Choose the number generation range ({} or greater): 1 and... ".format(numMax))
    number = int(number)
    while number < numMax:
        print("Please enter a number {} or greater".format(numMax))
        number = int(input("Choose the number generation range (Larger than {}): 1 and... ".format(numMax)))
    while number > 1000000: 
        print("Number too big!")
        number = int(input("Choose the number generation range (Larger than {}): 1 and... ".format(numMax)))
        
    return number
    


names = []

def runGame(number):
    global attempts
    global name
    
    attempts = 0
    
    name = input("Hello, What is your name? ")
    names.append(name)
    print("Hello " + name + "." )

    global randomChoice
    global tries
    
    randomChoice = random.randint(1, number)
    tries = math.ceil(math.log2(number))

    print("Generating random number...")
    time.sleep(0.5)
    print("You have {} tries!".format(tries))
    print("I am thinking of a number between 1 and", number)

    while tries > 0:
        guess = input("Have a guess: ")
        while guess.isdigit() == False:
            guess = input("Have a guess: ")
        guess = int(guess)

        if guess == randomChoice:
            break
        elif tries == 0:
            break
        elif guess < randomChoice:
            print("Guess Higher")
        elif guess > randomChoice:
            print("Guess Lower")
        tries -= 1
        attempts += 1
    
    if tries > 0:
        attempts += 1
        tries -=1 
        print("Congrats, you guessed correctly!")
        print("-" * 20 + "\nName: " + name + "\nDifficulty: " + difficulty.title() + "\nNumber range: 1 - " + str(numMax) + "\nNumber: " + str(randomChoice) + "\nAttempts: " + str(attempts) + "\nTries left: " + str(tries) + "\n" + "-" * 20)
    else:
        tries -=1
        print("Sorry, you ran out of tries! The correct number was {}".format(randomChoice))
        
    return tries

def runWithCount(count = 1):
    number = setupGame()
    scores = []
    
    for i in range(0, count):
        score = runGame(number)
        scores.append(score)
    if count == 1:
        savePlaySingle(name, difficulty , numMax, randomChoice, attempts, tries)
        return
    
    savePlayMulti(name, difficulty , numMax, randomChoice, attempts, tries)
    scores = [i for i in scores if i >= 0]
    global b
    a = zip(names, scores)
    b = sorted(a, key = lambda x: x[1])[::-1]

    print("Leaderboard")
    print("-" * 20)
    print ("{:<8} {:<15}".format("Name","Score"))
    for v in b:
        lname, score = v
        print ("{:<8} {:<15}".format(lname, score))

    
window = Tk()
window.title("Number Guessing Game")
window.geometry("175x110")
window.configure(bg="Light blue")

def multi():
    global playerCount
    window.geometry("300x205")
    Label(window, text="Enter amount of players playing", bg="Yellow", font=("Calibri 12")).pack()
    playerCountInput = Entry(window, width = 35, border = 5, bg="Light blue")
    playerCountInput.pack(pady=10)

    def start():
        try:
            playerCount = int(playerCountInput.get())
            runWithCount(playerCount)

        except ValueError:
            print("Please enter a valid number")
            
    Button(window, text = "Start", command = start, bg="Light green").pack()

def displayLeaderboard(difficulty):
    difWindow = Tk()
    difWindow.title("Leaderboards")
    
    difficulty = difficulty.capitalize()
    try:
        if os.stat("Leaderboard_" + difficulty + ".txt").st_size == 0:
            Label(difWindow, text="There are no scores\n saved in this leaderboard yet", font=("Calibri 12")).pack()
        with open("Leaderboard_" + difficulty + ".txt") as f:    
            lines = f.read()
        Label(difWindow, text=lines, font=("Calibri 12")).pack()
    except FileNotFoundError:
        Label(difWindow, text="There is no " + difficulty + " mode \nleaderboard yet", font=("Calibri 12")).pack()
        
def showLeaderboards():
    window = Tk()
    window.title("Guess the number leaderboard")
    window.geometry("200x115")
    window.configure(bg="Light green")
    
    easyLeaderboard = Button(window, text="Easy mode", bg="Light blue",command = lambda: displayLeaderboard("easy")).pack()
    mediumLeaderboard = Button(window, text="Medium mode", bg="Light blue",command = lambda: displayLeaderboard("medium")).pack()
    hardLeaderboard = Button(window, text="Hard mode", bg="Light blue",command = lambda: displayLeaderboard("hard")).pack()
    defaultLeaderboard = Button(window, text="Default mode", bg="Light blue",command = lambda: displayLeaderboard("default")).pack()
    
def displayScores(difficulty):
    difWindow = Tk()
    difWindow.title("User scores")
    difWindow.configure(bg="Yellow")

    directory = os.getcwd()
    filenames = []
    difLines = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filenames.append(filename)
    
    for filename in filenames:
        file = open(filename)
        lines = [1]
        for index, line in enumerate(file):
            if index in lines:
                try:
                    difLine = "".join(line.split(":")[1][1:len(line.split(":")[1])-1])
                    difLines.append(difLine)
                except IndexError:
                    pass
    
    if difficulty not in difLines:
        Label(difWindow, text="There are no user scores for \n" + difficulty + " mode yet", font=("Calibri 11")).pack()

    file_dif = list(zip(difLines, filenames))
    
    for i in file_dif:
        if i[0] == difficulty:
            f = open(i[1], "r")
            userLines = f.read()
            Label(difWindow, text=userLines, font=("Calirbi 9")).pack()
            
def showScores():
    window = Tk()
    window.title("Guess the number user scores")
    window.geometry("200x115")
    window.configure(bg="Light green")
    
    easyLeaderboard = Button(window, text="Easy mode", bg="Light blue",command = lambda: displayScores("easy")).pack()
    mediumLeaderboard = Button(window, text="Medium mode", bg="Light blue",command = lambda: displayScores("medium")).pack()
    hardLeaderboard = Button(window, text="Hard mode", bg="Light blue",command = lambda: displayScores("hard")).pack()
    defaultLeaderboard = Button(window, text="Default mode", bg="Light blue",command = lambda: displayScores("default")).pack()
        
SinglePlayer = Button(window, text="Single Player", bg="Light green",command = runWithCount).pack()
MultiPlayer = Button(window, text="Multi-Player", bg="Light green",command = multi).pack()
viewLeaderboards = Button(window, text="View leaderboards", bg="Light green",command = showLeaderboards).pack()
viewUserScores = Button(window, text="View user scores", bg="Light green",command = showScores).pack()

window.mainloop()
    
