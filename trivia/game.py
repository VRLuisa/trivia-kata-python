MAX_PLAYERS = 6
MINIMUM_PLAYERS = 2
QUESTIONS_PER_CATEGORY = 50
BOARD_SIZE = 12
WINNING_COINS = 6
CATEGORIES = ["Pop", "Science", "Sports", "Rock"]

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 1
        self.coins = 0
        self.in_penalty_box = False

class QuestionDeck:
    def __init__(self):
        self.questions_by_category = {
            "Pop": [],
            "Science": [],
            "Sports": [],
            "Rock": [],
        }
        self.create_questions()

    def create_questions(self):
        for i in range(QUESTIONS_PER_CATEGORY):
            self.questions_by_category["Pop"].append("Pop Question " + str(i))
            self.questions_by_category["Science"].append("Science Question " + str(i))
            self.questions_by_category["Sports"].append("Sports Question " + str(i))
            self.questions_by_category["Rock"].append(self.create_rock_question(i))

    def create_rock_question(self, index):
        return "Rock Question " + str(index)

    def next_question_for(self, category):
        return self.questions_by_category[category].pop(0)

class Game:
    def __init__(self):
        self.players = []

        self.current_player_index = 0
        self.is_getting_out_of_penalty_box = False

        self.question_deck = QuestionDeck()


    def isPlayable(self):
        return self.howManyPlayers() >= MINIMUM_PLAYERS

    def add(self, playerName):
        self.players.append(Player(playerName))

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
        return self.players[self.current_player_index].name
    
    def current_player_position(self):
        return self.players[self.current_player_index].position
    
    def award_coin_to_current_player(self):
        current_player = self.players[self.current_player_index]
        current_player.coins += 1

        print(
            self.current_player_name()
            + " now has "
            + str(current_player.coins)
            + " Gold Coins."
        )

    def finish_turn_after_correct_answer(self):
        winner = self.didPlayerWin()
        self.advance_to_next_player()
        return winner
    
    def handle_current_player_correct_answer(self, answer_message):
        print(answer_message)
        self.award_coin_to_current_player()
        return self.finish_turn_after_correct_answer()

    def current_player_is_in_penalty_box(self):
        return self.players[self.current_player_index].in_penalty_box
    
    def move_current_player(self, roll):
        current_player = self.players[self.current_player_index]
        current_player.position = current_player.position + roll

        if current_player.position > BOARD_SIZE:
            current_player.position = current_player.position - BOARD_SIZE
    
    def show_location_and_ask_question(self):
        print(
            self.current_player_name()
            + "'s new location is "
            + str(self.current_player_position())
        )
        print("The category is " + self.current_category())
        self.ask_question()

    def handle_normal_turn(self, roll):
        self.move_current_player(roll)
        self.show_location_and_ask_question()

    def handle_penalty_box_turn(self, roll):
        if self.can_get_out_of_penalty_box(roll):
            self.is_getting_out_of_penalty_box = True

            print(self.current_player_name() + " is getting out of the penalty box")
            self.move_current_player(roll)
            self.show_location_and_ask_question()
        else:
            print(self.current_player_name() + " is not getting out of the penalty box")
            self.is_getting_out_of_penalty_box = False

    def can_get_out_of_penalty_box(self, roll):
        return roll % 2 != 0

    def roll(self, roll):
        print(self.current_player_name() + " is the current player")
        print("They have rolled a " + str(roll))

        if self.current_player_is_in_penalty_box():
            self.handle_penalty_box_turn(roll)
        else:
            self.handle_normal_turn(roll)

    def next_question_for(self, category):
        return self.question_deck.next_question_for(category)

    def ask_question(self):
        category = self.current_category()
        print(self.next_question_for(category))

    def current_category(self):
        position_index = self.current_player_position() - 1
        category_index = position_index % len(CATEGORIES)

        return CATEGORIES[category_index]

    def handleCorrectAnswer(self):
        if self.current_player_is_in_penalty_box():
            if self.is_getting_out_of_penalty_box:
                return self.handle_current_player_correct_answer("Answer was correct!!!!")
            else:
                self.advance_to_next_player()
                return True

        else:
            return self.handle_current_player_correct_answer("Answer was corrent!!!!")

    def wrongAnswer(self):
        print("Question was incorrectly answered")
        print(self.current_player_name() + " was sent to the penalty box")
        self.players[self.current_player_index].in_penalty_box = True

        self.advance_to_next_player()
        return True

    def didPlayerWin(self):
        return not (self.players[self.current_player_index].coins == WINNING_COINS)