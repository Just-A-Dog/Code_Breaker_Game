import tkinter as tk
import random
import itertools

COLORS = ["red", "blue", "yellow", "green"]
ALL_COMBOS = list(itertools.product(COLORS, repeat=4))


def evaluate(solution, guess):
    stars = sum(a == b for a, b in zip(solution, guess))

    sol_counts = {}
    guess_counts = {}

    for c in solution:
        sol_counts[c] = sol_counts.get(c, 0) + 1

    for c in guess:
        guess_counts[c] = guess_counts.get(c, 0) + 1

    total = 0
    for c in sol_counts:
        if c in guess_counts:
            total += min(sol_counts[c], guess_counts[c])

    dots = total - stars
    return stars, dots


def count_valid_solutions(hints, results):

    valid = []

    for candidate in ALL_COMBOS:

        works = True

        for hint, result in zip(hints, results):

            if evaluate(candidate, hint) != result:
                works = False
                break

        if works:
            valid.append(candidate)

    return valid


def generate_puzzle():

    solution = random.choice(ALL_COMBOS)

    while True:

        hints = [random.choice(ALL_COMBOS) for _ in range(4)]
        results = [evaluate(solution, hint) for hint in hints]

        valid = count_valid_solutions(hints, results)

        if len(valid) == 1:
            return solution, hints, results


class PuzzleGame:

    def __init__(self, root):

        self.root = root
        self.root.title("Color Puzzle")

        self.create_ui()
        self.new_puzzle()

    def create_ui(self):

        self.hint_tiles = []
        self.hint_results = []

        for r in range(4):

            row_tiles = []

            for c in range(4):

                label = tk.Label(self.root, width=4, height=2, relief="ridge")
                label.grid(row=r, column=c, padx=3, pady=3)

                row_tiles.append(label)

            result = tk.Label(self.root, text="", width=6)
            result.grid(row=r, column=5, padx=10)

            self.hint_tiles.append(row_tiles)
            self.hint_results.append(result)

        self.player = ["red"] * 4
        self.player_buttons = []

        for i in range(4):

            btn = tk.Button(
                self.root,
                width=4,
                height=2,
                bg=self.player[i],
                command=lambda i=i: self.cycle_color(i)
            )

            btn.grid(row=5, column=i, pady=10)

            self.player_buttons.append(btn)

        self.check_button = tk.Button(self.root, text="Check", command=self.check_solution)
        self.check_button.grid(row=6, column=0, columnspan=2)

        self.new_button = tk.Button(self.root, text="New Puzzle", command=self.new_puzzle)
        self.new_button.grid(row=6, column=2, columnspan=2)

        self.status = tk.Label(self.root, text="")
        self.status.grid(row=7, column=0, columnspan=4)

    def cycle_color(self, index):

        current = COLORS.index(self.player[index])
        new = (current + 1) % len(COLORS)

        self.player[index] = COLORS[new]

        self.player_buttons[index].config(bg=self.player[index])

    def new_puzzle(self):

        self.solution, self.hints, self.results = generate_puzzle()

        for r in range(4):

            for c in range(4):

                color = self.hints[r][c]
                self.hint_tiles[r][c].config(bg=color)

            stars, dots = self.results[r]
            text = "★" * stars + " •" * dots

            self.hint_results[r].config(text=text)

        self.status.config(text="")

        self.player = ["red"] * 4

        for i in range(4):
            self.player_buttons[i].config(bg="red")

    def check_solution(self):

        if tuple(self.player) == self.solution:
            self.status.config(text="Solved!")
        else:
            self.status.config(text="Not correct")


root = tk.Tk()
game = PuzzleGame(root)
root.mainloop()