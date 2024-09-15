import random
import time
import matplotlib.pyplot as plt

# Card Deck Constants
CARD_DISTRIBUTION = {
    -2: 5,
    -1: 10,
    0: 15,
    1: 10,
    2: 10,
    3: 10,
    4: 10,
    5: 10,
    6: 10,
    7: 10,
    8: 10,
    9: 10,
    10: 10,
    11: 10,
    12: 10,
}

# Create deck of cards
def create_deck():
    deck = []
    for card_value, count in CARD_DISTRIBUTION.items():
        deck.extend([card_value] * count)
    random.shuffle(deck)
    return deck

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.grid = [[None for _ in range(4)] for _ in range(3)]
        self.face_up = [[False for _ in range(4)] for _ in range(3)]
        self.revealed = 0
        self.score = 0

    def set_initial_grid(self, deck):
        # Deal 12 cards to the player's grid
        for i in range(3):
            for j in range(4):
                self.grid[i][j] = deck.pop()

    def reveal_two_initial_cards(self):
        # Player randomly reveals two cards
        for _ in range(2):
            i, j = random.randint(0, 2), random.randint(0, 3)
            if not self.face_up[i][j]:
                self.face_up[i][j] = True
                self.revealed += 1

    def reveal_card(self, i, j):
        if not self.face_up[i][j]:
            self.face_up[i][j] = True
            self.revealed += 1
            return self.grid[i][j]
        return None

    def exchange_card(self, i, j, new_card):
        old_card = self.grid[i][j]
        self.grid[i][j] = new_card
        if not self.face_up[i][j]:
            self.face_up[i][j] = True
            self.revealed += 1
        return old_card

    def check_vertical_triple(self):
        # Check if any vertical column has the same card and remove it
        for j in range(4):
            if self.face_up[0][j] and self.face_up[1][j] and self.face_up[2][j]:
                if self.grid[0][j] == self.grid[1][j] == self.grid[2][j]:
                    for i in range(3):
                        self.grid[i][j] = None
                        self.face_up[i][j] = False

    def calculate_score(self):
        # Calculate the player's score based on their revealed cards
        total_score = 0
        for i in range(3):
            for j in range(4):
                if self.grid[i][j] is not None:
                    total_score += self.grid[i][j]
        self.score = total_score  # Update score directly
        return total_score

    def choose_card_position(self):
        # Enhanced strategic approach: Prioritize replacing the worst card (highest value) with a good card.
        worst_value = float('-inf')
        worst_pos = None

        for i in range(3):
            for j in range(4):
                if self.face_up[i][j] and self.grid[i][j] is not None and self.grid[i][j] > worst_value:
                    worst_value = self.grid[i][j]
                    worst_pos = (i, j)

        return worst_pos if worst_pos else (random.randint(0, 2), random.randint(0, 3))

    def decide_card_action(self, drawn_card):
        """
        Decides what to do with a drawn card.
        - Keep low-value cards and replace the worst.
        - Discard high-value cards and reveal a new card.
        """
        if drawn_card <= 3:
            i, j = self.choose_card_position()
            return "keep", (i, j)
        else:
            return "discard", (random.randint(0, 2), random.randint(0, 3))

class SkyjoGame:
    def __init__(self, num_players=6):
        self.deck = create_deck()
        self.players = [Player(f'Player {i+1}') for i in range(num_players)]
        self.discard_pile = []
        self.rounds_played = 0
        self.scores = []
        self.winner = None
        self.round_ended = False

    def start_game(self):
        for player in self.players:
            player.set_initial_grid(self.deck)
            player.reveal_two_initial_cards()

    def play_turn(self, player):
        # Player draws a card from the deck
        if not self.deck:
            if self.discard_pile:
                self.deck = self.discard_pile[:-1]  # Leave the top discard card
                random.shuffle(self.deck)
                self.discard_pile = [self.discard_pile[-1]]  # Keep the top discard card
            else:
                raise RuntimeError("No cards left in the deck or discard pile!")

        drawn_card = self.deck.pop()
        action, position = player.decide_card_action(drawn_card)

        if action == "keep":
            i, j = position
            discarded = player.exchange_card(i, j, drawn_card)
            self.discard_pile.append(discarded)
        elif action == "discard":
            self.discard_pile.append(drawn_card)
            i, j = position
            player.reveal_card(i, j)

        player.check_vertical_triple()

    def play_round(self):
        self.rounds_played += 1
        round_ended = False
        player_that_ended_round = None

        # Continue playing until a player has revealed all 12 cards
        while not round_ended:
            for player in self.players:
                if player.revealed == 12:
                    round_ended = True
                    player_that_ended_round = player
                    break
                self.play_turn(player)

        # After the round ends, give all other players one final turn
        for player in self.players:
            if player != player_that_ended_round:
                self.play_turn(player)

        self.round_ended = True

    def calculate_final_scores(self):
        for player in self.players:
            player.calculate_score()
        self.scores.append([(player.name, player.score) for player in self.players])

    def play_game(self):
        self.start_game()
        game_over = False

        # Continue playing rounds until a player reaches or exceeds 100 points
        while not game_over:
            self.play_round()
            self.calculate_final_scores()

            # Check if any player has reached or exceeded 100 points
            if any(player.score >= 100 for player in self.players):
                game_over = True  # Break the game loop if any player reaches 100+ points
            elif self.round_ended:  # End the game after the final round
                break

        # Determine the winner
        self.winner = min(self.players, key=lambda player: player.score)
        return self.winner, self.rounds_played, self.scores[-1]

    def simulate_games(self, num_simulations):
        win_counts = {player.name: 0 for player in self.players}
        total_scores = {player.name: 0 for player in self.players}
        all_scores = {player.name: [] for player in self.players}

        for _ in range(num_simulations):
            game = SkyjoGame()
            winner, _, final_scores = game.play_game()

            # Track wins
            win_counts[winner.name] += 1

            # Track scores and accumulate total scores
            for player_name, score in final_scores:
                total_scores[player_name] += score
                all_scores[player_name].append(score)

        # Calculate average scores
        avg_scores = {player_name: total_scores[player_name] / num_simulations for player_name in total_scores}

        return win_counts, avg_scores, all_scores

    def visualize_simulation_results(self, num_simulations, win_counts, avg_scores, all_scores):
        # Visualize win distribution
        plt.figure(figsize=(10, 6))
        plt.bar(win_counts.keys(), win_counts.values(), color='lightblue')
        plt.title(f"Win Distribution Over {num_simulations} Simulations")
        plt.xlabel("Players")
        plt.ylabel("Number of Wins")
        plt.show()

        # Visualize average scores
        plt.figure(figsize=(10, 6))
        plt.bar(avg_scores.keys(), avg_scores.values(), color='lightgreen')
        plt.title(f"Average Scores Over {num_simulations} Simulations")
        plt.xlabel("Players")
        plt.ylabel("Average Score")
        plt.show()

        # Visualize score distribution for each player
        for player_name, scores in all_scores.items():
            plt.figure(figsize=(10, 6))
            plt.hist(scores, bins=20, color='lightcoral', edgecolor='black')
            plt.title(f"Score Distribution for {player_name} Over {num_simulations} Simulations")
            plt.xlabel("Score")
            plt.ylabel("Frequency")
            plt.show()

# Simulate N games and visualize results
num_simulations = 1000
game = SkyjoGame()
win_counts, avg_scores, all_scores = game.simulate_games(num_simulations)
game.visualize_simulation_results(num_simulations, win_counts, avg_scores, all_scores)
