import random


class AI:
    def __init__(self, epsilion:float = 0.1, training:bool = False):
        self.epsilion = epsilion
        self.field = []
        self.who = "X"
        self.q_table = {}
        self.last_state = None
        self.last_action = None
        self.training = training
        
    def is_first_move(self) -> bool:
        pass
    
    def create_field(self) -> list:
        return [" "] * 9
        
    def get_state(self) -> str:
        return "".join(self.field)
        
    def get_emptys(self) -> list:
        return [i for i, f in enumerate(self.field) if f == " "]
        
    def get_q(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0] * 9
        return self.q_table[state]
        
    def check_winner(self):
        w = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]

        for a,b,c in w:
            #wenn Kombination gefunden & nicht leer = Gewinner
            if self.field[a] == self.field[b] == self.field[c] != " ":
                return self.field[a]

        if " " not in self.field:
            return "draw"
            
        #Spiel läuft noch
        return None
        
    def update_q(self, reward, next_state):
        alpha = 0.1   # Lernrate
        gamma = 0.9   # Zukunftswert wichtigkeit

        old_q = self.q_table[self.last_state][self.last_action]
        max_future = max(self.get_q(next_state))

        self.q_table[self.last_state][self.last_action] = old_q + alpha * (
            reward + gamma * max_future - old_q
        )
    def reset(self):
        self.field = self.create_field()
        self.who = "X"
        self.last_state = None
        self.last_action = None
    
    def print_field(self):
        print("\n")
        for i in range(0, 9, 3):
            print(f"{self.field[i]} | {self.field[i+1]} | {self.field[i+2]}")
            if i < 6:
                print("--+---+--")
        print("\n")
    
    def human_move(self):
        empty = self.get_emptys()
    
        while True:
            try:
                move = int(input(f"Wähle ein Feld {empty}: "))
                if move in empty:
                    return move
                print("Ungültiger Zug!")
            except ValueError:
                print("Bitte Zahl eingeben!")
    
    def play(self) -> None:
        if not self.field:
            self.field = self.create_field()
    
        state = self.get_state()
        empty = self.get_emptys()
        q_values = self.get_q(state)
    

        if not self.training and self.who == "O":
            move = self.human_move()
        else:

            if random.random() < self.epsilion and self.training:
                move = random.choice(empty)
            else:
                move = max(empty, key=lambda i: q_values[i])
    
        self.last_state = state
        self.last_action = move
        self.field[move] = self.who
    
        result = self.check_winner()
        
        #Ende
        if result is not None:
            if self.last_state is not None and self.last_action is not None and self.training:
                reward = 0
                if result == "draw":
                    reward = 0
                elif result == self.who:
                    reward = 1
                else:
                    reward = -1
    
                self.update_q(reward, self.get_state())
            if not self.training:
                self.print_field()
                print("Result:", result)
            return
        else:
            # Zwischenupdate für q_table
            pass
    
        self.who = "O" if self.who == "X" else "X"
        
        
ai = AI(training=True)

for episode in range(1,100001):
    ai.reset()

    for _ in range(9):
        ai.play()
        if ai.check_winner() is not None:
            break

    print(f"{episode}", end="\r")
#print(ai.q_table)

#selbst spielen
ai.training = False
ai.epsilion = 0.0

print("\n")
ai.reset()

while True:
    ai.play()
    if ai.check_winner() is not None:
        input("enter für nächstes Spiel")
        ai.reset()
    ai.print_field()
