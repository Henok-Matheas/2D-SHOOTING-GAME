from turtle import width
import pygame
from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
from PIL import Image

vao, space_vao, program, texture, space_texture = None, None, None, None, None

WIDTH, HEIGHT = 900, 600


def getFileContents(filename):
    p = os.path.join(os.getcwd(), "Assets", "shaders", filename)
    return open(p, 'r').read()


def init():
    global vao, space_vao, program, texture, space_texture
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

    # SINGLE IMAGE
    vertexes = np.array([
        # position          # color           # texture s, r
        [0.25, 0.25, -.50,    1.0, 0.20, 0.8, 1.0, 1.0],
        [0.25, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-0.25, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],

        [0.25, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [-0.25, -0.25, -.50,  0.0, 0.4, 1.0, 0.0, 0.0],
        [-0.25, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)
    glBindVertexArray(vao)

    positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    colorLocation = glGetAttribLocation(program, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    textLocation = glGetAttribLocation(program, "texCoord")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                          8 * vertexes.itemsize, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # LOADING IMAGE
    image = Image.open("Assets/images/shotgun.jpg")
    width, height = image.width, image.height
    image_data = np.array(list(image.getdata()), dtype=np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    # unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # unbind VAO
    glBindVertexArray(0)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    # ___________________________END___________________________

    # SINGLE IMAGE
    space_vertexes = np.array([
        # position          # color           # texture s, r
        [0.85, 0.25, -.50,    1.0, 0.20, 0.8, 1.0, 1.0],
        [0.85, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [0.35, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],

        [0.85, -0.25, -.50,   1.0, 1.0, 0.0, 1.0, 0.0],
        [0.35, -0.25, -.50,  0.0, 0.4, 1.0, 0.0, 0.0],
        [0.35, 0.25, -.50,   0.0, 0.7, 0.2, 0.0, 1.0],
    ], dtype=np.float32)

    space_vao = glGenVertexArrays(1)
    space_vbo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, space_vbo)
    glBufferData(GL_ARRAY_BUFFER, space_vertexes.nbytes,
                 space_vertexes, GL_STATIC_DRAW)
    glBindVertexArray(space_vao)

    space_positionLocation = glGetAttribLocation(program, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          8 * space_vertexes.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    space_colorLocation = glGetAttribLocation(program, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          8 * space_vertexes.itemsize, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    space_textLocation = glGetAttribLocation(program, "texCoord")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                          8 * space_vertexes.itemsize, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    space_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, space_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # LOADING IMAGE
    space_image = Image.open(
        "Assets/images/rifle.jpg")
    space_image = space_image.crop((20, 20, 300, 200))
    # space_image = space_image.resize(size=(40, 40), box=(20, 20, 60, 60))
    # space_image.show()
    width, height = space_image.width, space_image.height
    space_image_data = np.array(list(space_image.getdata()), dtype=np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, space_image_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    # unbind VBO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # unbind VAO
    glBindVertexArray(0)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    # ___________________________END___________________________


def draw():
    global vao, space_vao, program, texture, space_texture
    glClear(GL_COLOR_BUFFER_BIT)
    # glEnable(GL_BLEND)
    glUseProgram(program)

    # FOR SINGLE IMAGE
    glBindVertexArray(vao)
    glBindTexture(GL_TEXTURE_2D, texture)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)
    # END

    # FOR SINGLE IMAGE
    glBindVertexArray(space_vao)
    glBindTexture(GL_TEXTURE_2D, space_texture)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)
    # END


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("the window has been closed")
                quit()
        draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()
