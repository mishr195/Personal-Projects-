
def print_board(board):
        for i in range(0, 9, 3):
            print(" | ".join(board[i:i+3]))
            if i < 6:
                print("-" * 9)

def check_win(player, board):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]

        for combo in winning_combinations:
            if all(board[i] == player for i in combo):
                return True
        return False

def check_tie(board):
        return "-" not in board

def player_input(player, board):
        while True:
            try:
                move = int(input(f"Player {player}, choose a position (1-9): "))
                if 1 <= move <= 9 and board[move - 1] == "-":
                    return move - 1
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 1 and 9.")

def switch_player(player):
        return "X" if player == "O" else "O"

def player_game():
        board = ["-" for _ in range(9)]
        current_player = "X"
        game_running = True

        # Start the game loop
        while game_running:
            print_board(board)
            move = player_input(current_player, board)
            board[move] = current_player

            if check_win(current_player, board):
                print_board(board)
                print(f"Player {current_player} wins!")
                game_running = False
            elif check_tie(board):
                print_board(board)
                print("It's a tie!")
                game_running = False
            else:
                current_player = switch_player(current_player)

def computer_game():
        def computer_move(board, current_player):
            if current_player == "O":
                best_score = -float("inf")
                best_move = None

                for i in range(9):
                    if board[i] == "-":
                        board[i] = "O"
                        score = minimax(board, 0, False)
                        board[i] = "-"
                        if score > best_score:
                            best_score = score
                            best_move = i

                return best_move

        def minimax(board, depth, is_maximizing):
            scores = {"X": -1, "O": 1, "tie": 0}
            winner = None

            if check_win("X", board):
                winner = "X"
            elif check_win("O", board):
                winner = "O"
            elif check_tie(board):
                winner = "tie"

            if winner:
                return scores[winner]

            if is_maximizing:
                best_score = -float("inf")
                for i in range(9):
                    if board[i] == "-":
                        board[i] = "O"
                        score = minimax(board, depth + 1, False)
                        board[i] = "-"
                        best_score = max(score, best_score)
                return best_score
            else:
                best_score = float("inf")
                for i in range(9):
                    if board[i] == "-":
                        board[i] = "X"
                        score = minimax(board, depth + 1, True)
                        board[i] = "-"
                        best_score = min(score, best_score)
                return best_score

        # Initialize game variables
        board = ["-" for _ in range(9)]
        user_choice = "yes"

        computer_playing = user_choice.lower().startswith("y")

        if computer_playing:
            current_player = "X"
            computer_player = "O"
        else:
            current_player = "X"

        game_running = True

        # Start the game loop
        while game_running:
            print_board(board)

            if current_player == computer_player:
                move = computer_move(board, current_player)
                print("")
                print("")
            else:
                move = player_input(current_player, board)

            board[move] = current_player

            if check_win(current_player, board):
                print_board(board)
                if computer_playing and current_player == computer_player:
                    print("Computer wins! Congratulations, you've been outwitted by a bunch of ones and zeros!")
                else:
                    print(f"Player {current_player} wins! Savior of the humanity")
                game_running = False
            elif check_tie(board):
                print_board(board)
                print("It's a tie! You can't win, This is the best you will do!!!")
                game_running = False
            else:
                current_player = switch_player(current_player)

if __name__ == "__main__":
        user_choice = input("Do you want to play against a computer? (yes/no): ").lower()
        if user_choice == "yes":
            computer_game()
        elif user_choice == "no":
            player_game()
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

