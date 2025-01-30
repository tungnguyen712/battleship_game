import matplotlib.pyplot as plt
import numpy as np
import random
from minimax import *
import copy

def draw_board(board_size, hits, misses, title="Battleship Game Board", ax=None):
    """Draws/updates the board without surrounding borders"""
    if ax is None:
        ax = plt.gca()
    else:
        ax.clear()

    # Remove all axis borders and ticks
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(which='both', length=0)

    ax.set_yticks([])
    ax.set_xticks([])
    
    # Draw internal grid lines only
    for x in range(1, board_size):
        ax.axvline(x=x, color='black', linewidth=1, alpha=0.5)
    for y in range(1, board_size):
        ax.axhline(y=y, color='black', linewidth=1, alpha=0.5)

    # Add labels inside the grid (fixed coordinates)
    for i in range(board_size):
        # Column letters (top, y=0.1 instead of -0.1)
        ax.text(i + 0.5, 0.1, chr(65+i), ha='center', va='center', fontsize=9)
        # Row numbers (left, x=0.1 instead of -0.1)
        ax.text(0.1, i + 0.5, str(i+1), ha='center', va='center', fontsize=9)

    # Set tight limits
    ax.set_xlim(0, board_size)
    ax.set_ylim(board_size, 0)
    ax.set_aspect('equal')

    # Draw hits and misses (existing code remains)
    for (row, col) in hits:
        x, y = col + 0.5, row + 0.5
        circle = plt.Circle((x, y), 0.3, color='red', alpha=0.5)
        ax.add_patch(circle)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            dx = 0.4 * np.cos(angle)
            dy = 0.4 * np.sin(angle)
            ax.plot([x, x+dx], [y, y+dy], 'r-', lw=1.5)

    for (row, col) in misses:
        ax.text(col + 0.5, row + 0.5, '○', color='blue', 
               fontsize=16, ha='center', va='center')

    ax.set_title(title, fontsize=14, pad=15)
    plt.tight_layout()
    plt.draw()
    plt.pause(0.001)

def create_board(size):
    return [['~' for _ in range(size)] for _ in range(size)]

def place_ship(board, ship_length):
    direction = random.choice(['H', 'V'])
    placed = False
    while not placed:
        if direction == 'H':
            row = random.randint(0, len(board)-1)
            col = random.randint(0, len(board)-ship_length)
            if all(board[row][col+i] == '~' for i in range(ship_length)):
                for i in range(ship_length):
                    board[row][col+i] = 'S'
                placed = True
        else:
            row = random.randint(0, len(board)-ship_length)
            col = random.randint(0, len(board)-1)
            if all(board[row+i][col] == '~' for i in range(ship_length)):
                for i in range(ship_length):
                    board[row+i][col] = 'S'
                placed = True

def result(board, row, col, hits, misses):
    if board[row][col] == 'S':
        print("Hit!")
        hits.append((row, col))
        board[row][col] = 'X'
    elif board[row][col] == '~':
        print("Miss!")
        misses.append((row, col))
        board[row][col] = 'O'
    else:
        print("Already guessed this location!")
    return board

def get_player_input(player_name):
    while True:
        guess = input(f"{player_name}, enter your guess (e.g., A5): ").upper().strip()
        if len(guess) < 2 or not guess[0].isalpha() or not guess[1:].isdigit():
            print("Invalid format. Use letter followed by number (e.g., A5)")
            continue
        col = ord(guess[0]) - 65
        row = int(guess[1:]) - 1
        if 0 <= row < 10 and 0 <= col < 10:
            return row, col
        print("Coordinates out of range. Use A-J and 1-10")

def main():
    plt.ion()  # Enable interactive mode
    fig = None
    ax = None
    
    print("Welcome to Battleship!")
    board_size = 10

    # Initialize game state
    player_boards = [create_board(board_size), create_board(board_size)]
    player_hits = [[], []]
    player_misses = [[], []]

    # Place ships for both players
    for player in range(2):
        for ship_len in [5, 4, 3, 3, 2]:
            place_ship(player_boards[player], ship_len)

    current_player = 0
    game_mode = input("Choose game mode (1: Human vs Human, 2: Human vs Bot): ")

    while True:
        opponent = 1 - current_player

        # Initialize figure on first move
        if fig is None:
            fig = plt.figure(figsize=(7, 7), facecolor='white')
            ax = fig.add_subplot(111)
    
        # Bot's turn
        if game_mode == '2' and current_player == 1:  # Bot's turn
            print("\nBot's thinking...")
            ai_move = minimax(player_boards[opponent], player_hits[1], player_misses[1])
            if ai_move:
                result(player_boards[opponent], ai_move[0], ai_move[1], player_hits[1], player_misses[1])
            
            # Update display
            draw_board(board_size, player_hits[1], player_misses[1], "Your Ships (Bot's Attacks)", ax)
            plt.pause(1)
            
        else:  # Human's turn
            draw_board(board_size, player_hits[current_player], player_misses[current_player], f"Player {opponent+1}'s Board", ax)
            
            row, col = get_player_input(f"Player {current_player+1}")
            result(player_boards[opponent], row, col, player_hits[current_player], player_misses[current_player])

        # Check win condition
        if terminal(player_boards[opponent]):
            draw_board(board_size, player_hits[current_player], player_misses[current_player], f"Final Board - Player {current_player+1} Wins!", ax)
            if game_mode == '1':
                print(f"\nPlayer {current_player+1} wins!")
            else:
                # In game_mode 2, current_player 0 is Human, 1 is Bot
                if current_player == 0:
                    print("\nPlayer 1 wins!")
                else:
                    print("\nBot wins!")
            plt.ioff()
            plt.show(block=True)
            break

        current_player = 1 - current_player

if __name__ == "__main__":
    main()
