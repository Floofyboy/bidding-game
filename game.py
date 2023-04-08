import random

class Fighter:
    def __init__(self):
        self.hp = random.randint(20, 100)
        self.attack = random.randint(5, 20)

    def __str__(self):
        return f"{self.hp}/{self.attack}"

    def strength(self):
        return self.hp + self.attack

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.gold = 100
        self.army = []
        self.is_ai = is_ai

    def __str__(self):
        return self.name

    def make_bid(self, fighter, remaining_fighters, fighter_number, opponent_gold):
        if self.is_ai:
            max_strength = 100 * 20
            modified_strength = fighter.hp * fighter.attack

            relative_strength = modified_strength / max_strength
            gold_per_fighter = (self.gold + opponent_gold) / remaining_fighters * 1

            # Increase the bid based on the fighter's strength and AI aggression
            bid = int(gold_per_fighter * relative_strength * 2.3)
            if self.gold > opponent_gold * remaining_fighters:
                bid = int(self.gold / remaining_fighters)

            # Ensure the bid does not exceed the AI's available gold
            bid = min(self.gold, bid)

            # Ensure the bid is at least 1
            if self.gold > 0:
                bid = max(1, bid)
            else:
                bid = 0  # Set the bid to 0 if the AI has no gold left
            if bid > opponent_gold:
                bid = opponent_gold + 1
        else:
            bid = int(input(f"{self.name}, enter your bid for Fighter {fighter_number} (HP: {fighter.hp}, Attack: {fighter.attack}): "))
            bid = min(self.gold, bid)
        return bid
        
class Player3(Player):
    def make_bid(self, fighter, remaining_fighters, fighter_number, opponent_gold):
        if self.is_ai:
            max_strength = 100 * 20
            modified_strength = fighter.hp * fighter.attack

            relative_strength = modified_strength / max_strength
            gold_per_fighter = (self.gold + opponent_gold) / remaining_fighters * 0.95

            # Increase the bid based on the fighter's strength and AI aggression
            bid = int(gold_per_fighter * relative_strength * 2.3)
            if self.gold > opponent_gold * remaining_fighters:
                bid = int(self.gold / remaining_fighters)

            # Ensure the bid does not exceed the AI's available gold.
            bid = min(self.gold, bid)

            # Ensure the bid is at least 1
            if self.gold > 0:
                bid = max(1, bid)
            else:
                bid = 0  # Set the bid to 0 if the AI has no gold left
            if bid > opponent_gold:
                bid = opponent_gold + 1
        else:
            bid = int(input(f"{self.name}, enter your bid for Fighter {fighter_number} (HP: {fighter.hp}, Attack: {fighter.attack}): "))
            bid = min(self.gold, bid)
        return bid

def auction(player1, player2, fighter, remaining_fighters, fighter_number):
    bid1 = player1.make_bid(fighter, remaining_fighters, fighter_number, player2.gold)
    bid2 = player2.make_bid(fighter, remaining_fighters, fighter_number, player1.gold)

    print(f"{player1.name} bid: {bid1}, {player2.name} bid: {bid2}")

    if bid1 > bid2 and player1.gold >= bid1:
        player1.gold -= bid1
        player1.army.append(fighter)
        print(f"{player1.name} won the auction for Fighter {fighter_number} (HP: {fighter.hp}, Attack: {fighter.attack}).")
    elif bid2 > bid1 and player2.gold >= bid2:
        player2.gold -= bid2
        player2.army.append(fighter)
        print(f"{player2.name} won the auction for Fighter {fighter_number} (HP: {fighter.hp}, Attack: {fighter.attack}).")
    else:
        print(f"No one won the auction for Fighter {fighter_number} (HP: {fighter.hp}, Attack: {fighter.attack}).")

    print(f"{player1.name} gold left: {player1.gold}, {player2.name} gold left: {player2.gold}")

def battle(player1, player2):
    if player1.gold > player2.gold:
        attacker, defender = player1, player2
    else:
        attacker, defender = player2, player1

    while attacker.army and defender.army:
        attacker.army[0].hp -= defender.army[0].attack
        if attacker.army[0].hp <= 0:
            attacker.army.pop(0)
        if not attacker.army:
            break

        defender.army[0].hp -= attacker.army[0].attack
        if defender.army[0].hp <= 0:
            defender.army.pop(0)

    if len(attacker.army) > len(defender.army):
        return attacker
    else:
        return defender

def visualize_armies(player1, player2):
    army1_str = " + ".join(str(fighter) for fighter in player1.army)
    army2_str = " + ".join(str(fighter) for fighter in player2.army)
    print(f"{army1_str} vs {army2_str}")

def main(is_ai=False):
    player1 = Player("Player 1")
    if is_ai:
        player2 = Player("AI Player 1", is_ai=True)
        player3 = Player3("AI Player 2", is_ai=True)

        fighters = [Fighter() for _ in range(10)]
        for i, fighter in enumerate(fighters):
            remaining_fighters = len(fighters) - i
            fighter_number = i + 1
            auction(player2, player3, fighter, remaining_fighters, fighter_number)

        print("\nFinal armies:")
        visualize_armies(player2, player3)

        winner = battle(player2, player3)
        print(f"\n{winner.name} wins the game!")
    else:
        player2 = Player("AI Player", is_ai=True)

        fighters = [Fighter() for _ in range(10)]
        for i, fighter in enumerate(fighters):
            remaining_fighters = len(fighters) - i
            fighter_number = i + 1
            auction(player1, player2, fighter, remaining_fighters, fighter_number)

        print("\nFinal armies:")
        visualize_armies(player1, player2)

        winner = battle(player1, player2)
        print(f"\n{winner.name} wins the game!")

if __name__ == "__main__":
    # Set is_ai to True for AI vs AI, False for human vs AI
    main(is_ai=False)