from OpenGL.GL import *
from pygame.locals import *
from OpenGL.GL.shaders import *
import numpy as np
import os
from PIL import Image


class Menu_Object:

    def __init__(self, vertexes, image, program) -> None:
        self.image_location = image
        self.program = program
        self.texture = None
        self.vertexes = vertexes
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertexes.nbytes,
                     vertexes, GL_STATIC_DRAW)
        glBindVertexArray(self.vao)

        positionLocation = glGetAttribLocation(self.program, "position")
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                              8 * self.vertexes.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        colorLocation = glGetAttribLocation(self.program, "color")
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                              8 * self.vertexes.itemsize, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        textLocation = glGetAttribLocation(self.program, "texCoord")
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                              8 * self.vertexes.itemsize, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # LOADING IMAGE
        self.image = Image.open(os.path.join("Assets", "images", image))
        width, height = self.image.width, self.image.height
        self.image_data = np.array(list(self.image.getdata()), dtype=np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGB, GL_UNSIGNED_BYTE, self.image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        # unbind VBO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        # unbind VAO
        glBindVertexArray(0)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # ___________________________END___________________________

    def getFileContents(self, filename):
        p = os.path.join(os.getcwd(), "Assets", "shaders", filename)
        return open(p, 'r').read()
