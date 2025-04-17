from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, canvas, snake_coords):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake_coords:
                break

        self.coordinates = [x, y]
        self.food = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


class Game:
    def __init__(self, window):
        self.window = window
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        self.score = 0
        self.direction = 'down'

        self.label = Label(window, text="Score: 0", font=('consolas', 40))
        self.label.pack()

        self.canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.window.update()

        self.center_window()

        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))
        self.window.bind('<r>', lambda event: self.restart_game())

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake.coordinates)

        self.running = True
        self.next_turn()

    def center_window(self):
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def next_turn(self):
        if not self.running:
            return

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        new_head = [x, y]
        self.snake.coordinates.insert(0, new_head)
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.snake.squares.insert(0, square)

        if new_head == self.food.coordinates:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas, self.snake.coordinates)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)

    def change_direction(self, new_direction):
        opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        if self.snake.coordinates[0] in self.snake.coordinates[1:]:
            return True

        return False

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.canvas.winfo_width() / 2,
                                self.canvas.winfo_height() / 2,
                                font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
        self.running = False

    def restart_game(self):
        self.canvas.delete(ALL)
        self.label.config(text="Score: 0")
        self.score = 0
        self.direction = 'down'
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake.coordinates)
        self.running = True
        self.next_turn()


if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    # Pic = PhotoImage(pass)
    root.mainloop()
