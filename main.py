import random

import pygame
import pymunk

pygame.init()

space = pymunk.Space()
space.gravity = (0,100)

display = pygame.display.set_mode((800,800))
pygame.display.set_caption("Physics Engine")
clock = pygame.time.Clock()
bg = pygame.image.load("bg.png")
bg_resized = pygame.transform.scale(bg, (1000, 1000))

cube_size = 30

color = "red"
object_ = "circle"


class Button:
    def __init__(self, surface : pygame.surface, left: int, top: int, width: int, height: int, color, text=None, text_pos_x=None, text_pos_y=None, text_color=(255,255,255), font_size=None, font_bold=False,image=None, image_pos_x=None, image_pos_y=None) -> None:
        """
        :param surface: pygame surface
        :param left: The rectangle's left position : int
        :param top: The rectangle's right position : int
        :param width: The rectangle's width position : int
        :param height: The rectangle's height position : int
        :param color: The rectangle's color : str : (int, int,int) : hex
        :param text: The buttons text : str
        :param text_pos_x: The x position of the text : int
        :param text_pos_y: The y position of the text : int
        :param text_color: The color of the text : tuple
        :param font_size: The font size of the text : str
        :param font_bold: Boldness of the font : str
        :param image: Path of the image : str
        :param image_pos_x: The x position of the image : int
        :param image_pos_y: The y position of the image : int
        """
        self.surface = surface
        self.color = color
        self.rect = pygame.Rect(left,top, width, height)
        self.image = image
        self.text = text
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        self.font_size = font_size
        self.font_bold = font_bold
        self.text_color = text_color
        self.image_pos_x = image_pos_x
        self.image_pos_y = image_pos_y


    def draw(self, update_text = False, updated_text = None, update_text_position=False, updated_text_pos_x = None, updated_text_pos_y = None) -> None:
        """

        :param update_text: update the text of the current button: bool
        :param updated_text: the new text you want to draw on the button : str : int
        :param update_text_position: update the position of the current button's text : bool
        :param updated_text_pos_x: updates the text's x position : int
        :param updated_text_pos_y: updates the text's y position : int
        :return: None
        """
        if self.image is None and self.text is None:
            pygame.draw.rect(display,self.color, self.rect)

        elif self.image is None:
            self.font = pygame.font.SysFont("Bold", int(self.font_size), self.font_bold)

            if update_text is True:
                if updated_text is None:
                    raise Exception("Updated text argument is missing")
                else:
                    if update_text_position is False:
                        self.new_text = self.font.render(str(updated_text), True, self.text_color)
                        pygame.draw.rect(display, self.color, self.rect)
                        self.surface.blit(self.new_text, (self.text_pos_x, self.text_pos_y))

                    if update_text_position is True:
                        self.new_text = self.font.render(str(updated_text), True, self.text_color)
                        pygame.draw.rect(display, self.color, self.rect)
                        self.surface.blit(self.new_text, (updated_text_pos_x, updated_text_pos_y))

            else:
                self.new_text = self.font.render(str(self.text), True, self.text_color)
                pygame.draw.rect(display, self.color, self.rect)
                self.surface.blit(self.new_text, (self.text_pos_x, self.text_pos_y))

        else:
            display.blit(self.image, (self.image_pos_x, self.image_pos_y))

    def on_colision(self,func) -> None:
        func()

    def check_collision(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x,y):
            return True
        else:
            return False

change_object_button =  Button(display, left=650, top=150, width=80, height=30, color="blue", text=f"Object: {object_}", text_pos_x=655, text_pos_y=160, font_size=15)
spawn_button = Button(display, 650, 200, 90, 30, "blue", "Stress Test Mode", 655, 210, font_size=15)


change_object_button_clicks = 0

class Ball:
    def __init__(self, color, position, elasticity, radius):
        self.body = pymunk.Body(1, 1, body_type=pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, radius)
        self.color = color
        self.shape.elasticity = elasticity
        self.body.position = position
        self.radius = radius
        space.add(self.body,self.shape)

    def draw(self) -> None:
        pygame.draw.circle(display, self.color, (self.body.position.x, self.body.position.y), radius=self.radius)

class Outline:
    def __init__(self, a, b, radius, color):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, a, b, radius)
        self.a = a
        self.b = b
        self.radius = radius
        self.color = color
        space.add(self.shape, self.body)

    def draw(self) -> None:
        pygame.draw.line(display, self.color, self.a, self.b, self.radius)

class Square:
    def __init__(self, p1, p2, radius, color):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC, mass=1, moment=1)
        self.radius = radius
        self.color = color
        self.a = p1
        self.b = p2
        self.shape = pymunk.Segment(self.body, p1, p2, self.radius)
        self.shape.friction = 10
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.line(display, self.color, self.a, self.b, self.radius)

class Poly:
    def __init__(self, points):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC, mass=1, moment=1)
        self.points = points
        self.shape = pymunk.Poly(self.body, self.points, radius=10)
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.polygon(display, "red", self.points,)

floor = Outline((1, 500), (580, 500), 7, "white")
wall_left = Outline((1, 500), (1, 1), 6, "white")
wall_right = Outline((580,500), (580,1), 5, "white")

ball_list = []
outline_list = []
square_list = []
polygon_list = []

fps_font = pygame.font.SysFont("Bold", 30, False, False)

clicked = False

while True:
    display.fill("black")

    spawn_button.draw()

    fps = fps_font.render(str(int(clock.get_fps())), False, (255,255,255))

    for outline in outline_list:
        outline.draw()

    for ball in ball_list:
        ball.draw()

    for square in square_list:
        square.draw()

    for polygon in polygon_list:
        polygon.draw()

    if change_object_button_clicks == 0:
        change_object_button.draw()

    if change_object_button_clicks == 1:
        object_ = "square"
        change_object_button.draw(True, "Object: square", True, 655, 160)

    if change_object_button_clicks == 2:
        object_ = "poly"
        change_object_button.draw(True, "Object: polygon", True, 655, 160)

    x, y = mouse_pos = pygame.mouse.get_pos()

    if change_object_button.check_collision(x, y):
        if clicked is True:
            change_object_button_clicks += 1
            clicked = False

    if spawn_button.check_collision(x, y):
        for i in range(1000):
            if clicked:
                ball_list.append(Ball("red", (random.randint(30,300), random.randint(30, 500)), 0, 15))

    floor.draw()
    wall_left.draw()
    wall_right.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if object_ == "circle":
                    if not clicked:
                        ball_list.append(Ball("red", pygame.mouse.get_pos(), 2, 15))
                        clicked = True

                elif object_ == "square":
                        square_list.append(Square((x+10, y), (x+10, y+cube_size), 30, "red"))
                        clicked = True

                elif object_ == "poly":
                    polygon_list.append(Poly([(x+180,y+80), (x+30, y+20), (x+100, y+100)],))
                    clicked = True

            if event.button == 3:
                if object_ == "circle":
                        square_list.append(Square((x + 10, y), (x + 10, y + cube_size), 30, "red"))
                        clicked = True

                elif object_ == "square":
                        ball_list.append(Ball("red", pygame.mouse.get_pos(), 2, 15))
                        clicked = True

                elif object_ == "poly":
                    ball_list.append(Ball("red", pygame.mouse.get_pos(), 2, 15))
                    clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit(-1)

    display.blit(fps, (750,30))
    space.step(1/50)
    clock.tick(60)
    pygame.display.update()
