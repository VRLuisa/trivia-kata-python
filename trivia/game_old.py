class GameOld:
    def __init__(self):
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.inPenaltyBox = [False] * 6

        self.popQuestions = []
        self.scienceQuestions = []
        self.sportsQuestions = []
        self.rockQuestions = []

        self.currentPlayer = 0
        self.isGettingOutOfPenaltyBox = False

        for i in range(50):
            self.popQuestions.append("Pop Question " + str(i))
            self.scienceQuestions.append("Science Question " + str(i))
            self.sportsQuestions.append("Sports Question " + str(i))
            self.rockQuestions.append(self.createRockQuestion(i))

    def createRockQuestion(self, index):
        return "Rock Question " + str(index)

    def isPlayable(self):
        return self.howManyPlayers() >= 2

    def add(self, playerName):
        self.places[self.howManyPlayers()] = 1
        self.purses[self.howManyPlayers()] = 0
        self.inPenaltyBox[self.howManyPlayers()] = False
        self.players.append(playerName)

        print(playerName + " was added")
        print("They are player number " + str(len(self.players)))
        return True

    def howManyPlayers(self):
        return len(self.players)

    def roll(self, roll):
        print(self.players[self.currentPlayer] + " is the current player")
        print("They have rolled a " + str(roll))

        if self.inPenaltyBox[self.currentPlayer]:
            if roll % 2 != 0:
                self.isGettingOutOfPenaltyBox = True

                print(self.players[self.currentPlayer] + " is getting out of the penalty box")
                self.places[self.currentPlayer] = self.places[self.currentPlayer] + roll
                if self.places[self.currentPlayer] > 12:
                    self.places[self.currentPlayer] = self.places[self.currentPlayer] - 12

                print(
                    self.players[self.currentPlayer]
                    + "'s new location is "
                    + str(self.places[self.currentPlayer])
                )
                print("The category is " + self.currentCategory())
                self.askQuestion()
            else:
                print(self.players[self.currentPlayer] + " is not getting out of the penalty box")
                self.isGettingOutOfPenaltyBox = False

        else:
            self.places[self.currentPlayer] = self.places[self.currentPlayer] + roll
            if self.places[self.currentPlayer] > 12:
                self.places[self.currentPlayer] = self.places[self.currentPlayer] - 12

            print(
                self.players[self.currentPlayer]
                + "'s new location is "
                + str(self.places[self.currentPlayer])
            )
            print("The category is " + self.currentCategory())
            self.askQuestion()

    def askQuestion(self):
        if self.currentCategory() == "Pop":
            print(self.popQuestions.pop(0))
        if self.currentCategory() == "Science":
            print(self.scienceQuestions.pop(0))
        if self.currentCategory() == "Sports":
            print(self.sportsQuestions.pop(0))
        if self.currentCategory() == "Rock":
            print(self.rockQuestions.pop(0))

    def currentCategory(self):
        if self.places[self.currentPlayer] - 1 == 0:
            return "Pop"
        if self.places[self.currentPlayer] - 1 == 4:
            return "Pop"
        if self.places[self.currentPlayer] - 1 == 8:
            return "Pop"
        if self.places[self.currentPlayer] - 1 == 1:
            return "Science"
        if self.places[self.currentPlayer] - 1 == 5:
            return "Science"
        if self.places[self.currentPlayer] - 1 == 9:
            return "Science"
        if self.places[self.currentPlayer] - 1 == 2:
            return "Sports"
        if self.places[self.currentPlayer] - 1 == 6:
            return "Sports"
        if self.places[self.currentPlayer] - 1 == 10:
            return "Sports"
        return "Rock"

    def handleCorrectAnswer(self):
        if self.inPenaltyBox[self.currentPlayer]:
            if self.isGettingOutOfPenaltyBox:
                print("Answer was correct!!!!")
                self.purses[self.currentPlayer] += 1
                print(
                    self.players[self.currentPlayer]
                    + " now has "
                    + str(self.purses[self.currentPlayer])
                    + " Gold Coins."
                )

                winner = self.didPlayerWin()
                self.currentPlayer += 1
                if self.currentPlayer == len(self.players):
                    self.currentPlayer = 0

                return winner
            else:
                self.currentPlayer += 1
                if self.currentPlayer == len(self.players):
                    self.currentPlayer = 0
                return True

        else:
            print("Answer was correct!!!!")
            self.purses[self.currentPlayer] += 1
            print(
                self.players[self.currentPlayer]
                + " now has "
                + str(self.purses[self.currentPlayer])
                + " Gold Coins."
            )

            winner = self.didPlayerWin()
            self.currentPlayer += 1
            if self.currentPlayer == len(self.players):
                self.currentPlayer = 0

            return winner

    def wrongAnswer(self):
        print("Question was incorrectly answered")
        print(self.players[self.currentPlayer] + " was sent to the penalty box")
        self.inPenaltyBox[self.currentPlayer] = True

        self.currentPlayer += 1
        if self.currentPlayer == len(self.players):
            self.currentPlayer = 0
        return True

    def didPlayerWin(self):
        return not (self.purses[self.currentPlayer] == 6)