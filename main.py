import pygame
import pymunk

pygame.init()

space = pymunk.Space()
space.gravity = (0,100)

display = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
bg = pygame.image.load("bg.png")
bg_resized = pygame.transform.scale(bg, (1000,1000))


color = "red"

class Button:
    def __init__(self, surface : pygame.surface, left, top, width, height, color, text=None, text_pos_x=None, text_pos_y=None, text_color=(255,255,255), font_size=None, font_bold=False,image=None, image_pos_x=None, image_pos_y=None) -> None:
        """
        :param surface: pygame surface
        :param left: The rectangle's left position -> int
        :param top: The rectangle's right position -> int
        :param width: The rectangle's width position -> int
        :param height: The rectangle's height position -> int
        :param color: The rectangle's color -> (str, tuple, int)
        :param text: The buttons text -> str
        :param text_pos_x: The x position of the text -> int
        :param text_pos_y: The y position of the text -> int
        :param text_color: The color of the text -> tuple
        :param font_size: The font size of the text -> str
        :param font_bold: Boldness of the font -> bool
        :param image: Path of the image -> str
        :param image_pos_x: The x position of the image -> int
        :param image_pos_y: The y position of the image -> int
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

    def draw(self) -> None:
        if self.image is None and self.text is None:
            pygame.draw.rect(display,self.color, self.rect)

        elif self.image is None:
            self.font = pygame.font.SysFont("Bold",int(self.font_size), self.font_bold)
            self.new_text = self.font.render(str(self.text), True, self.text_color)

            pygame.draw.rect(display, self.color, self.rect)
            self.surface.blit(self.new_text, (self.text_pos_x, self.text_pos_y))

        else:
            display.blit(self.image, (self.image_pos_x, self.image_pos_y))

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

floor = Outline((1, 500), (700, 500), 5, "white")

ball_list = []
outline_list = []

while True:
    display.fill("black")

    for outline in outline_list:
        outline.draw()

    for ball in ball_list:
        ball.draw()

    floor.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if color == "red":
                    ball_list.append(Ball("red", pygame.mouse.get_pos(), 2, 15))
            if event.button == 3:
                if color == "red":
                    outline_list.append(Outline((100,300), (300,100), 10, "red"))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit(-1);

    space.step(1/50)
    clock.tick(60)
    pygame.display.update()
