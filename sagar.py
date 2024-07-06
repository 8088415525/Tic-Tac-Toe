from tkinter import Tk, Button
import random

# Define game board and current player
board = [' ' for _ in range(9)]
current_player = 'X'

# Function to check if a player has won
def check_winner():
    winning_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]
    for row in winning_conditions:
        if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
            return board[row[0]]
    return None

# Function to check if the board is full (tie)
def check_board_full():
    return all(cell != ' ' for cell in board)

# Function to get available moves
def get_available_moves():
    return [(row, col) for row in range(3) for col in range(3) if board[row * 3 + col] == ' ']

# AI easy level
def ai_easy():
    available_moves = get_available_moves()
    chosen_move = random.choice(available_moves)
    row, col = chosen_move
    board_index = row * 3 + col
    board[board_index] = 'O'
    buttons[board_index].config(text='O', fg='red')

# Function to evaluate the board for the AI player (maximizing score)
def evaluate():
    scores = {'X': 1, 'O': -1, ' ': 0}
    lines = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]
    player_score = 0
    opponent_score = 0
    for line in lines:
        if line == ['X', 'X', 'X']:
            return 1000
        if line == ['O', 'O', 'O']:
            return -1000
        player_score += line.count('X') * scores['X']
        opponent_score += line.count('O') * scores['O']
    return player_score + opponent_score

# Function to find the best move for the AI
def find_best_move(maximizing_player):
    best_score = -float('inf') if maximizing_player else float('inf')
    best_move = None
    available_moves = get_available_moves()
    for move in available_moves:
        row, col = move
        index = row * 3 + col
        board[index] = 'X' if maximizing_player else 'O'
        score = minimax(0, not maximizing_player)
        board[index] = ' '
        if maximizing_player and score > best_score:
            best_score = score
            best_move = move
        elif not maximizing_player and score < best_score:
            best_score = score
            best_move = move
    return best_move

# Minimax algorithm to evaluate the best score
def minimax(depth, maximizing_player):
    score = evaluate()
    if abs(score) == 1000 or not get_available_moves():
        return score
    if maximizing_player:
        max_eval = -float('inf')
        for move in get_available_moves():
            row, col = move
            index = row * 3 + col
            board[index] = 'X'
            eval = minimax(depth + 1, False)
            board[index] = ' '
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves():
            row, col = move
            index = row * 3 + col
            board[index] = 'O'
            eval = minimax(depth + 1, True)
            board[index] = ' '
            min_eval = min(min_eval, eval)
        return min_eval

# Function to handle button click
def button_click(button_number):
    global current_player, board
    if board[button_number] == ' ':
        board[button_number] = current_player
        buttons[button_number].config(text=current_player, fg='blue' if current_player == 'X' else 'red')
        winner = check_winner()
        if winner:
            show_message(f"Player {winner} wins!")
            disable_buttons()
        elif check_board_full():
            show_message("It's a tie!")
            disable_buttons()
        else:
            if ai == 1:
                show_message(f"AI's turn")
                ai_easy()
                aip_win()
            elif ai == 2:
                show_message(f"AI's turn")
                best_move = find_best_move(False)
                if best_move:
                    row, col = best_move
                    board_index = row * 3 + col
                    board[board_index] = 'O'
                    buttons[board_index].config(text='O', fg='red')
                aip_win()
            else:
                current_player = 'X' if current_player == 'O' else 'O'
                show_message(f"Player {current_player}'s turn")

# Function to check winner after AI move
def aip_win():
    winner = check_winner()
    if winner:
        show_message(f"Player {winner} wins!")
        disable_buttons()
    elif check_board_full():
        show_message("It's a tie!")
        disable_buttons()

# Function to disable buttons after game ends
def disable_buttons():
    for button in buttons:
        button.config(state='disabled')

# Function to show message
def show_message(message):
    message_label.config(text=message)

# Function to restart the game
def restart_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    show_message(f"Player {current_player}'s turn")
    for button in buttons:
        button.config(text=' ', state='normal', fg='black')

# Create the main window
window = Tk()
window.title("Tic Tac Toe")

# Create a label for current player
message_label = Button(window, text=f"Player {current_player}'s turn", font=('Arial', 16), state='disabled')
message_label.grid(row=0, column=0, columnspan=3)

# Create buttons for the game board
buttons = []
for row in range(3):
    for col in range(3):
        button_number = row * 3 + col
        button = Button(window, text=' ', font=('Arial', 24), width=3, height=1,
                        command=lambda btn_num=button_number: button_click(btn_num))
        button.grid(row=row + 1, column=col)
        buttons.append(button)

# Create a restart button
restart_button = Button(window, text="Restart", font=('Arial', 12), command=restart_game)
restart_button.grid(row=4, column=0, columnspan=3)

# Function to start the game based on player's choice
def entry():
    print("1. Both Players \n2. AI")
    en = int(input())
    if en == 2:
        print("1. Normal \n2. Hard")
        ai_level = int(input())
        main("Player V/S AI", ai_level)
    else:
        main("Player V/S Player", 0)

# Run the main loop
def main(whose, ai_mode):
    global ai
    ai = ai_mode
    show_message(f"Player {current_player}'s turn")
    window.mainloop()

entry()
