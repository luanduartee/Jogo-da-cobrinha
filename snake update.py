"""Esse é o jogo da cobra em uma versão pyxel!

Tente coletar as maçãs, enquanto a cobra corre, sem 
encostar nas bordas ou em si mesmo.

Controle o movimento da cobra usando as setas ← ↑ → ↓ do teclado

Q: Sair do jogo
R: Reiniciar o jogo

"""

from collections import deque, namedtuple
from random import randint

import pyxel

Point = namedtuple("Point", ["x", "y"])


#############
# Variáveis #
#############

COL_BACKGROUND = 11
COL_BODY = 2
COL_HEAD = 2
COL_DEATH = 8
COL_APPLE = 8

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 7
HEIGHT_DEATH = 9

WIDTH = 50
HEIGHT = 50

HEIGHT_SCORE = pyxel.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)

START = Point(5, 5 + HEIGHT_SCORE)


##################
#  O jogo em si  #
##################


class Game:
    """A classe que define a estrutura do jogo."""

    def __init__(self):
        """Iniciar o pyxel, configurar as variáveis iniciais do jogo e executar.
        É o construtor da classe Game"""

        pyxel.init(WIDTH, HEIGHT, caption="Cobrinha!", fps=20)
        define_sound_and_music()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Inicia as variáveis (direção, maçã, pontuação, cobra, etc.)"""

        self.direction = RIGHT
        self.snake = deque()
        self.snake.append(START)
        self.death = False
        self.score = 0
        self.generate_apple()

        pyxel.playm(0, loop=True)

    ##################
    # Lógica do Jogo #
    ##################

    def update(self):
        """Atualiza a lógica do jogo. Atualiza a cobra e verifica a pontuação/vitória"""

        if not self.death:
            self.update_direction()
            self.update_snake()
            self.check_death()
            self.check_apple()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_direction(self):
        """Muda a direção da cobra."""

        if pyxel.btn(pyxel.KEY_UP):
            if self.direction is not DOWN:
                self.direction = UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.direction is not UP:
                self.direction = DOWN
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.direction is not RIGHT:
                self.direction = LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.direction is not LEFT:
                self.direction = RIGHT

    def update_snake(self):
        """Move a cobra baseado na direção."""

        old_head = self.snake[0]
        new_head = Point(old_head.x + self.direction.x, old_head.y + self.direction.y)
        self.snake.appendleft(new_head)
        self.popped_point = self.snake.pop()

    def check_apple(self):
        """Verifica se a cobra comeu a maçã."""

        if self.snake[0] == self.apple:
            self.score += 1
            self.snake.append(self.popped_point)
            self.generate_apple()

            pyxel.play(0, 0)

    def generate_apple(self):
        """Gera uma maçã aleatoriamente."""
        snake_pixels = set(self.snake)

        self.apple = self.snake[0]
        while self.apple in snake_pixels:
            x = randint(0, WIDTH - 1)
            y = randint(HEIGHT_SCORE + 1, HEIGHT - 1)
            self.apple = Point(x, y)

    def check_death(self):
        """Verifica se a cobra morreu (fora das margens ou dobrada)."""

        head = self.snake[0]
        if head.x < 0 or head.y <= HEIGHT_SCORE or head.x >= WIDTH or head.y >= HEIGHT:
            self.death_event()
        elif len(self.snake) != len(set(self.snake)):
            self.death_event()

    def death_event(self):
        """Acabar o jogo (Abrir a tela final)."""
        self.death = True  # Verifica se ele bateu em si mesmo

        pyxel.stop()
        pyxel.play(0, 1)

    ##############
    # Desenhando #
    ##############

    def draw(self):
        """Desenha o plano de fundo, a cobra, a pontuação, a maçã e a tela final."""

        if not self.death:
            pyxel.cls(col=COL_BACKGROUND)
            self.draw_snake()
            self.draw_score()
            pyxel.pset(self.apple.x, self.apple.y, col=COL_APPLE)

        else:
            self.draw_death()

    def draw_snake(self):
        """Desenha a cobra com a cabeça distinta/separada."""

        for i, point in enumerate(self.snake):
            if i == 0:
                colour = COL_HEAD
            else:
                colour = COL_BODY
            pyxel.pset(point.x, point.y, col=colour)

    def draw_score(self):
        """Desenha a pontuação no topo da janela."""

        score = "{:03}".format(self.score)
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        pyxel.text(1, 1, score, COL_SCORE)

    def draw_death(self):
        """Desenha uma tela em branco com um texto escrito."""

        pyxel.cls(col=COL_DEATH)
        display_text = TEXT_DEATH[:]
        display_text.insert(1, "{:03}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Função para calcular o valor inicial do x para texto centralizado."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2


############################
# Música e efeitos sonoros #
############################


def define_sound_and_music():
    """Define o som e a música."""

    # Efeitos sonoros
    pyxel.sound(0).set(
        note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
    )
    pyxel.sound(1).set(
        note="f3 b2 f2 b1  f1 f1 f1 f1",
        tone="p",
        volume=("4" * 4 + "4321"),
        effect=("n" * 7 + "f"),
        speed=9,
    )

    melody1 = (
        "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "e3 e3 e3 f3 d3 r c3 r"
        + ("r" * 8)
        + "c3 c3 c3 d3 e3 r e3 r"
        + ("r" * 8)
        + "b2 b2 b2 f3 d3 r c3 r"
        + ("r" * 8)
    )

    melody2 = (
        "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
        + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
        + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
        + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
        + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
    )

    # Música
    pyxel.sound(2).set(
        note=melody1 * 2 + melody2 * 2,
        tone="s",
        volume=("3"),
        effect=("nnnsffff"),
        speed=20,
    )

    harmony1 = (
        "a1 a1 a1 b1  f1 f1 c2 c2"
        "c2 c2 c2 c2  g1 g1 b1 b1" * 3
        + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
    )
    harmony2 = (
        ("f1" * 8 + "g1" * 8 + "a1" * 8 + ("c2" * 7 + "d2")) * 3 + "f1" * 16 + "g1" * 16
    )

    pyxel.sound(3).set(
        note=harmony1 * 2 + harmony2 * 2, tone="t", volume="5", effect="f", speed=20
    )
    pyxel.sound(4).set(
        note=("f0 r a4 r  f0 f0 a4 r" "f0 r a4 r   f0 f0 a4 f0"),
        tone="n",
        volume="6622 6622 6622 6426",
        effect="f",
        speed= 20,
    )

    pyxel.music(0).set([], [2], [3], [4])


Game()