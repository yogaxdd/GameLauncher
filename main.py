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
    result = c.fetchone()
    if result:
        path = result[0]
        if os.path.exists(path):
            os.startfile(path)  # Jalankan game
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Game file not found!")
    else:
        QtWidgets.QMessageBox.warning(None, "Selection Error", "No game selected!")

# Fungsi untuk update game (tampilkan notifikasi)
def update_game():
    QtWidgets.QMessageBox.information(None, "Update", "Update tidak tersedia, silahkan hubungi operator.")

# Fungsi untuk menutup aplikasi
def exit_app():
    app.quit()

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
window.setWindowTitle("YogaxD Game Launcher")
window.setGeometry(450, 220, 500, 400)
window.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    QLabel {
        font-size: 18px;
        font-weight: bold;
        color: #ffa500;
    }
    QListWidget {
        background-color: #3c3c3c;
        border: 1px solid #ffa500;
        color: #ffffff;
        padding: 5px;
    }
    QPushButton {
        background-color: #ffa500;
        color: #ffffff;
        border: none;
        padding: 10px;
        font-size: 14px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #ff8c00;
    }
    QPushButton:pressed {
        background-color: #e67600;
    }
    QLabel#versionLabel {
        font-size: 12px;
        color: #aaaaaa;
    }
""")

# Layout utama
layout = QtWidgets.QVBoxLayout()

# Label "YogaxD Game Launcher"
header_label = QtWidgets.QLabel("YogaxD Game Launcher")
header_label.setAlignment(QtCore.Qt.AlignCenter)
layout.addWidget(header_label)

# List game
game_listbox = QtWidgets.QListWidget()
layout.addWidget(game_listbox)

# Layout untuk tombol
tombol_layout = QtWidgets.QHBoxLayout()

play_button = QtWidgets.QPushButton("Play")
play_button.clicked.connect(lambda: play_game(game_listbox.currentRow() + 1))
tombol_layout.addWidget(play_button)

update_button = QtWidgets.QPushButton("Update")
update_button.clicked.connect(update_game)
tombol_layout.addWidget(update_button)

exit_button = QtWidgets.QPushButton("Exit")
exit_button.clicked.connect(exit_app)
tombol_layout.addWidget(exit_button)

layout.addLayout(tombol_layout)

# Label "Versi 1.6"
version_label = QtWidgets.QLabel("Versi 1.6")
version_label.setObjectName("versionLabel")
version_label.setAlignment(QtCore.Qt.AlignCenter)
layout.addWidget(version_label)

# Set layout ke window
window.setLayout(layout)

# Update game list
update_game_list()

# Tampilin jendela
window.show()

# Mulai aplikasi
sys.exit(app.exec_())

# Jangan lupa tutup koneksi ke database saat aplikasi selesai
conn.close()
