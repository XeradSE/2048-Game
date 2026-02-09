import sys, logic2048, copy, configuration
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__() 

        self.game = logic2048.Game()

        self.setWindowTitle("2048 Python")
        self.setGeometry(100, 100, 400, 400) # x, y, w, h

        container = QWidget()
        self.setCentralWidget(container)

        self.layout = QGridLayout()
        container.setLayout(self.layout)

        self.update_interface()

    def update_interface(self):
        for i in range(len(self.game.grid)):
            for j in range(len((self.game.grid[0]))):
                value = self.game.grid[i][j]
                label_test = QLabel("")
                if value != 0:
                    label_test.setText(str(value))
                # 2. Gestion de la Couleur (Background)
                # .get(key, default) est très utile si tu dépasses 2048 (évite le crash)
                bg_color = configuration.TILE_COLORS.get(value, "#3c3a32") 
                
                # 3. Gestion de la Couleur du Texte
                text_color = configuration.LABEL_COLORS.get(value, "#f9f6f2") # Blanc par défaut
                style = f"""
                    QLabel {{
                        background-color: {bg_color};
                        color: {text_color};
                        border-radius: 5px;
                        font-size: 40px;
                        border: ipx solid black;
                    }}
                """
                label_test.setStyleSheet(style)
                label_test.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = label_test.font()
                font.setBold(True)
                label_test.setFont(font)
                self.layout.addWidget(label_test, i, j)

    def play_turn(self, direction):
        # 1. On fait une VRAIE copie de la grille
        grid_before = copy.deepcopy(self.game.grid)
        
        # 2. On tente le mouvement
        if direction == "left":
            self.game.move_left()
        elif direction == "right":
            self.game.move_right()
        elif direction == "up":
            self.game.move_up()
        else:
            self.game.move_down()
        
        # 3. On compare les valeurs
        if grid_before != self.game.grid:
            # Si ça a bougé, on ajoute une tuile ET on met à jour l'affichage
            self.game.add_new_tile()
            self.update_interface() # Ta méthode PyQt

    def keyPressEvent(self, event):
        # On récupère la touche pressée
        key = event.key()
        
        if key == Qt.Key.Key_Left:
            self.play_turn("left")
        elif key == Qt.Key.Key_Right:
            self.play_turn("right")
        elif key == Qt.Key.Key_Up:
            self.play_turn("up")
        elif key == Qt.Key.Key_Down:
            self.play_turn("down")

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())