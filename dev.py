import sys
import os
import sqlite3
from PyQt5 import QtWidgets, QtCore

# Koneksi ke database
conn = sqlite3.connect('games.db')
c = conn.cursor()

# Buat table game jika belum ada
c.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    name TEXT,
    path TEXT
)
''')
conn.commit()

# Fungsi untuk menjalankan game
def play_game(game_id):
    c.execute('SELECT path FROM games WHERE id = ?', (game_id,))
    path = c.fetchone()[0]
    if os.path.exists(path):
        os.startfile(path)  # Jalankan game
    else:
        QtWidgets.QMessageBox.critical(None, "Error", "Game file not found!")

# Fungsi untuk menambah game ke database
def add_game(name, path):
    if name and path:
        c.execute('INSERT INTO games (name, path) VALUES (?, ?)', (name, path))
        conn.commit()
        update_game_list()
    else:
        QtWidgets.QMessageBox.warning(None, "Input Error", "Please provide both name and path.")

# Fungsi untuk menghapus game dari database
def delete_game(game_id):
    c.execute('DELETE FROM games WHERE id = ?', (game_id,))
    conn.commit()
    update_game_list()

# Fungsi untuk update list game di UI
def update_game_list():
    game_listbox.clear()
    c.execute('SELECT id, name FROM games')
    games = c.fetchall()
    for game in games:
        game_listbox.addItem(game[1])

# Setup UI
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("YogaxD Game Launcher Developer")
window.setGeometry(300, 150, 500, 400)

# Label "YogaxD Game Data"
header_label = QtWidgets.QLabel("YogaxD Game Launcher Developer", window)
header_label.setAlignment(QtCore.Qt.AlignCenter)
header_label.setGeometry(50, 10, 400, 30)
header_label.setStyleSheet("font-size: 18px; font-weight: bold;")

# List game
game_listbox = QtWidgets.QListWidget(window)
game_listbox.setGeometry(50, 50, 400, 200)

# Tombol tambah game
name_input = QtWidgets.QLineEdit(window)
name_input.setPlaceholderText("Game Name")
name_input.setGeometry(50, 270, 200, 30)

path_input = QtWidgets.QLineEdit(window)
path_input.setPlaceholderText("Game Path")
path_input.setGeometry(50, 310, 200, 30)

add_button = QtWidgets.QPushButton("Add Game", window)
add_button.setGeometry(260, 270, 120, 30)
add_button.clicked.connect(lambda: add_game(name_input.text(), path_input.text()))

play_button = QtWidgets.QPushButton("Play Game", window)
play_button.setGeometry(260, 310, 120, 30)
play_button.clicked.connect(lambda: play_game(game_listbox.currentRow() + 1))

# Tombol untuk delete game
delete_button = QtWidgets.QPushButton("Delete Game", window)
delete_button.setGeometry(50, 350, 120, 30)
delete_button.clicked.connect(lambda: delete_game(game_listbox.currentRow() + 1))

# Update game list
update_game_list()

# Tampilin jendela
window.show()

# Mulai aplikasi
sys.exit(app.exec_())

# Jangan lupa tutup koneksi ke database saat aplikasi selesai
conn.close()
