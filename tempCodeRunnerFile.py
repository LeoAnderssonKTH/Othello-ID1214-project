 if (row, col) in valid_moves:
                    print(board.board[row][col + 1].color)
                    board.make_move(row, col)
                    break