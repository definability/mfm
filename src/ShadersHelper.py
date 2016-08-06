from os.path import dirname, abspath, join

from OpenGL.GL import glCreateProgram, glLinkProgram, glGetProgramiv
from OpenGL.GL import glGenVertexArrays, glBindVertexArray, glGenBuffers
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_LINK_STATUS
from OpenGL.GL import GL_TRUE, GL_STATIC_DRAW, GL_FLOAT, GL_FALSE
from OpenGL.GL import glBindBuffer, glBufferData, glVertexAttribPointer
from OpenGL.GL import glEnableVertexAttribArray, glGetAttribLocation
from OpenGL.GL import glCreateShader, glShaderSource, glCompileShader
from OpenGL.GL import glAttachShader, GL_ARRAY_BUFFER, glUseProgram
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glUniform1fv
from OpenGL.GL import glGenTextures, glPixelStorei, glTexParameterf
from OpenGL.GL import glBindTexture, glEnable, GL_UNPACK_ALIGNMENT
from OpenGL.GL import glUniform1i, GL_TEXTURE_1D, GL_TEXTURE_2D, GL_TEXTURE_3D
from OpenGL.GL import glTexImage1D, glTexImage2D, glTexImage3D, glDisable
from OpenGL.GL import GL_RED, GL_RG, GL_RGB, GL_RGBA
from OpenGL.GL import GL_R32F, GL_RG32F, GL_RGB32F, GL_RGBA32F
from OpenGL.GL import GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST


from OpenGL.arrays.vbo import VBO

from numpy import concatenate


SHADERS_PATH = dirname(abspath(__file__))


class ShadersHelper:
    """Helper class to work with program and shaders."""

    def __init__(self, vertex, fragment, number_of_buffers=0,
                 number_of_textures=0):
        """Initialize program with shaders."""
        self.__program = glCreateProgram()

        self.__load_shader(join(SHADERS_PATH, vertex), GL_VERTEX_SHADER)
        self.__load_shader(join(SHADERS_PATH, fragment), GL_FRAGMENT_SHADER)

        glLinkProgram(self.__program)
        assert glGetProgramiv(self.__program, GL_LINK_STATUS) == GL_TRUE

        self.__vao_id = glGenVertexArrays(1)
        glBindVertexArray(self.__vao_id)
        if number_of_buffers == 1:
            self.__vbo_id = [glGenBuffers(number_of_buffers)]
        elif number_of_buffers > 1:
            self.__vbo_id = glGenBuffers(number_of_buffers)

        self.__attributes = []

        if number_of_textures == 1:
            self.__textures_ids = [glGenTextures(1)]
        elif number_of_textures > 1:
            self.__textures_ids = glGenTextures(number_of_textures)
        self.__textures = []

    def __load_shader(self, shader_filename, shader_type):
        """Load shader of specific type from file."""
        shader_source = ''
        with open(shader_filename) as shader_file:
            shader_source = shader_file.read()
            assert shader_source

        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id, shader_source)
        glCompileShader(shader_id)
        glAttachShader(self.__program, shader_id)

    def add_attribute(self, vid, data, name):
        """Add array vertex attribute for shaders."""
        if data.ndim > 1:
            data = data.flatten()
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo_id[vid])
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        glVertexAttribPointer(glGetAttribLocation(self.__program, name),
                              3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(vid)
        self.__attributes.append(data)

    def use_shaders(self):
        """Switch shaders on."""
        glUseProgram(self.__program)
        glBindVertexArray(self.__vao_id)

    def bind_uniform_matrix(self, data, name):
        """Bind uniform matrix parameter."""
        location = glGetUniformLocation(self.__program, name)
        assert location >= 0
        glUniformMatrix4fv(location, 1, GL_FALSE, data.flatten())

    def bind_uniform_floats(self, data, name):
        location = glGetUniformLocation(self.__program, name)
        assert location >= 0
        glUniform1fv(location, data.size, data.flatten())

    def bind_buffer(self):
        """Prepare attributes and bind them."""
        VBO(concatenate(self.__attributes)).bind()

    def clear(self):
        """Unbind all bound entities and clear cache."""
        self.__attributes = []
        glUseProgram(0)
        glBindVertexArray(0)

    def bind_float_texture(self, data, name, size, dimensions=2, components=3):
        """Bind texture with floating point vectors within.

        dimensions: dimensionality of the texture
                    vector, matrix, 3D matrix.
        components: dimensionality of texture element
                    number or 2D, 3D, 4D vector.
        """
        if dimensions == 1:
            texture_type = GL_TEXTURE_1D
            texture_store = glTexImage1D
        elif dimensions == 2:
            texture_type = GL_TEXTURE_2D
            texture_store = glTexImage2D
        elif dimensions == 3:
            texture_type = GL_TEXTURE_3D
            texture_store = glTexImage3D

        if components == 1:
            internal_format = GL_R32F
            texture_format = GL_RED
        if components == 2:
            internal_format = GL_RG32F
            texture_format = GL_RG
        if components == 3:
            internal_format = GL_RGB32F
            texture_format = GL_RGB
        if components == 4:
            internal_format = GL_RGBA32F
            texture_format = GL_RGBA

        glBindTexture(texture_type, self.__textures_ids[len(self.__textures)])
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # HACK: Python <3.5 doesn't allow to use *size
        # within enumerable arguments
        params = ([texture_type, 0, internal_format]
                 + size + [0, texture_format, GL_FLOAT, data.flatten()])
        texture_store(*params)

        glEnable(texture_type)
        glTexParameterf(texture_type, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(texture_type, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.__textures.append(dimensions)

        location = glGetUniformLocation(self.__program, name)
        assert location >= 0
        glUniform1i(location, 0)
