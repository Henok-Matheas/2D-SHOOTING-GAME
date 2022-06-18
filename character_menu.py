from menu_object import Menu_Object
import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
from PIL import Image

vao, space_vao, program, texture, space_texture = None, None, None, None, None

WIDTH, HEIGHT = 600, 600


person_1 = None
person_2 = None
person_3 = None
person_4 = None
person_5 = None
person_6 = None


def getFileContents(filename):
    p = os.path.join(os.getcwd(), "Assets", "shaders", filename)
    return open(p, 'r').read()


def init():
    global program, person_1, person_2
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(.30, 0.20, 0.20, 1.0)
    glViewport(0, 0, WIDTH, HEIGHT)

    vertexShader = compileShader(getFileContents(
        "triangle.vertex.shader"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents(
        "triangle.fragment.shader"), GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)

    # SINGLE OBJECT
    person_1 = Menu_Object(np.array([
        # position          # color           # texture s, r
        [0.25, 0.25, -.50,    1.0, 0.20, 0.8, 1.0, 1.0],
        [0.25, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-0.25, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],

        [0.25, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-0.25, -0.25, -.50,  0.0, 0.4, 1.0, 0.0, 0.0],
        [-0.25, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],
    ], dtype=np.float32), "choice1.jpg", program)
    # END

    # SINGLE OBJECT
    person_2 = Menu_Object(np.array([
        # position          # color           # texture s, r
        [0.85, 0.25, -.50,    1.0, 0.20, 0.8, 1.0, 1.0],
        [0.85, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [0.35, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],

        [0.85, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [0.35, -0.25, -.50,  0.0, 0.4, 1.0, 0.0, 0.0],
        [0.35, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],
    ], dtype=np.float32), "choice2.jpg", program)
    # END


def draw():
    global program, person_1, person_2
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)

    # FOR A SINGLE OBJECT
    glBindVertexArray(person_1.vao)
    glBindTexture(GL_TEXTURE_2D, person_1.texture)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)
    # END

    # FOR A SINGLE OBJECT
    glBindVertexArray(person_2.vao)
    glBindTexture(GL_TEXTURE_2D, person_2.texture)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)
    # END


def char_menu():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.quit()
                    print(person_1.image_location)
                    return person_1.image_location
                if event.key == pygame.K_2:
                    pygame.quit()
                    return person_2.image_location
                # if event.key == pygame.K_3:
                #     pygame.quit()
                #     return person_3.image_location
                # if event.key == pygame.K_1:
                #     pygame.quit()
                #     return person_1.image_location
                # if event.key == pygame.K_1:
                #     pygame.quit()
                #     return person_1.image_location
                # if event.key == pygame.K_1:
                #     pygame.quit()
                #     return person_1.image_location
        draw()
        pygame.display.flip()
        pygame.time.wait(10)