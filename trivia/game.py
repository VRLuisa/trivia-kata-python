MAX_PLAYERS = 6
MINIMUM_PLAYERS = 2
QUESTIONS_PER_CATEGORY = 50
BOARD_SIZE = 12
WINNING_COINS = 6

class Game:
    def __init__(self):
        self.players = []
        self.player_positions  = [0] * MAX_PLAYERS
        self.player_coins = [0] * MAX_PLAYERS
        self.player_in_penalty_box = [False] * MAX_PLAYERS

        self.popQuestions = []
        self.scienceQuestions = []
        self.sportsQuestions = []
        self.rockQuestions = []

        self.current_player_index = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(QUESTIONS_PER_CATEGORY):
            self.popQuestions.append("Pop Question " + str(i))
            self.scienceQuestions.append("Science Question " + str(i))
            self.sportsQuestions.append("Sports Question " + str(i))
            self.rockQuestions.append(self.createRockQuestion(i))

    def createRockQuestion(self, index):
        return "Rock Question " + str(index)

    def isPlayable(self):
        return self.howManyPlayers() >= MINIMUM_PLAYERS

    def add(self, playerName):
        self.player_positions [self.howManyPlayers()] = 1
        self.player_coins[self.howManyPlayers()] = 0
        self.player_in_penalty_box[self.howManyPlayers()] = False
        self.players.append(playerName)

        print(playerName + " was added")
        print("They are player number " + str(len(self.players)))
        return True

    def howManyPlayers(self):
        return len(self.players)
    
    def advance_to_next_player(self):
        self.current_player_index += 1
        if self.current_player_index == len(self.players):
            self.current_player_index = 0
    
    def current_player_name(self):
        return self.players[self.current_player_index]
    
    def current_player_position(self):
        return self.player_positions[self.current_player_index]
    
    def move_current_player(self, roll):
        self.player_positions[self.current_player_index] = self.player_positions[self.current_player_index] + roll
        if self.player_positions[self.current_player_index] > BOARD_SIZE:
            self.player_positions[self.current_player_index] = self.player_positions[self.current_player_index] - BOARD_SIZE

    def show_location_and_ask_question(self):
        print(
            self.current_player_name()
            + "'s new location is "
            + str(self.current_player_position())
        )
        print("The category is " + self.currentCategory())
        self.askQuestion()

    def roll(self, roll):
        print(self.current_player_name() + " is the current player")
        print("They have rolled a " + str(roll))

        if self.player_in_penalty_box[self.current_player_index]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print(self.current_player_name() + " is getting out of the penalty box")
                self.move_current_player(roll)
                self.show_location_and_ask_question()
            else:
                print(self.current_player_name() + " is not getting out of the penalty box")
                self.is_getting_out_of_penalty_box = False

        else:
            self.move_current_player(roll)
            self.show_location_and_ask_question()

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
        if self.current_player_position() - 1 == 0:
            return "Pop"
        if self.current_player_position() - 1 == 4:
            return "Pop"
        if self.current_player_position() - 1 == 8:
            return "Pop"
        if self.current_player_position() - 1 == 1:
            return "Science"
        if self.current_player_position() - 1 == 5:
            return "Science"
        if self.current_player_position() - 1 == 9:
            return "Science"
        if self.current_player_position() - 1 == 2:
            return "Sports"
        if self.current_player_position() - 1 == 6:
            return "Sports"
        if self.current_player_position() - 1 == 10:
            return "Sports"
        return "Rock"

    def handleCorrectAnswer(self):
        if self.player_in_penalty_box[self.current_player_index]:
            if self.is_getting_out_of_penalty_box:
                print("Answer was correct!!!!")
                self.player_coins[self.current_player_index] += 1
                print(
                    self.current_player_name()
                    + " now has "
                    + str(self.player_coins[self.current_player_index])
                    + " Gold Coins."
                )

                winner = self.didPlayerWin()
                self.advance_to_next_player()

                return winner
            else:
                self.advance_to_next_player()
                return True

        else:
            print("Answer was corrent!!!!")
            self.player_coins[self.current_player_index] += 1
            print(
                self.current_player_name()
                + " now has "
                + str(self.player_coins[self.current_player_index])
                + " Gold Coins."
            )

            winner = self.didPlayerWin()
            self.advance_to_next_player()

            return winner

    def wrongAnswer(self):
        print("Question was incorrectly answered")
        print(self.current_player_name() + " was sent to the penalty box")
        self.player_in_penalty_box[self.current_player_index] = True

        self.advance_to_next_player()
        return True

    def didPlayerWin(self):
        return not (self.player_coins[self.current_player_index] == WINNING_COINS)