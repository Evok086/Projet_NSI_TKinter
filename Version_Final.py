import tkinter as tk
import chess
import chess.engine

class ChessApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Échecs")
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("/home/beauvivre/chess-env/stockfish-ubuntu-x86-64-sse41-popcnt/stockfish/stockfish-ubuntu-x86-64-sse41-popcnt")  # Remplacez par le chemin de votre moteur d'échecs

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#eee", "#ddd"]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color)

        for (piece, square) in self.board.piece_map().items():
            self.draw_piece(piece, square)

    def draw_piece(self, piece, square):
    # Convertir l'entier en objet de pièce
        piece_obj = chess.Piece(piece, chess.WHITE if piece > 0 else chess.BLACK)
        piece_symbol = piece_obj.symbol()
        col = chess.square_file(square)
        row = chess.square_rank(square)
        self.canvas.create_text(col * 50 + 25, (7 - row) * 50 + 25, text=piece_symbol, font=("Arial", 24))

    def on_click(self, event):
        col = event.x // 50
        row = 7 - (event.y // 50)
        square = chess.square(col, row)

        if self.board.is_legal(chess.Move.from_uci(self.last_move + chess.square_name(square))):
            self.board.push(chess.Move.from_uci(self.last_move + chess.square_name(square)))
            self.last_move = chess.square_name(square)
            self.draw_board()
            self.computer_move()

    def computer_move(self):
        if not self.board.is_game_over():
            result = self.engine.play(self.board, chess.engine.Limit(time=1.0))
            self.board.push(result.move)
            self.draw_board()

    def close(self):
        self.engine.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()