from OpenGL.GL import glCreateProgram, glLinkProgram, glGetProgramiv
from OpenGL.GL import glGenVertexArrays, glBindVertexArray, glGenBuffers
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_LINK_STATUS
from OpenGL.GL import GL_TRUE, GL_STATIC_DRAW, GL_FLOAT, GL_FALSE
from OpenGL.GL import glBindBuffer, glBufferData, glVertexAttribPointer
from OpenGL.GL import glEnableVertexAttribArray, glGetAttribLocation
from OpenGL.GL import glCreateShader, glShaderSource, glCompileShader
from OpenGL.GL import glAttachShader, GL_ARRAY_BUFFER, glUseProgram
from OpenGL.GL import glGetUniformLocation, glUniformMatrix4fv, glUniform1fv
from OpenGL.GL import glUniform1iv
from OpenGL.GL import glUniform4f
from OpenGL.GL import glGenTextures, glPixelStorei, glTexParameterf
from OpenGL.GL import glBindTexture, GL_UNPACK_ALIGNMENT
from OpenGL.GL import glUniform1i, GL_TEXTURE_1D, GL_TEXTURE_2D, GL_TEXTURE_3D
from OpenGL.GL import glTexImage1D, glTexImage2D, glTexImage3D
from OpenGL.GL import GL_RED, GL_RG, GL_RGB, GL_RGBA
from OpenGL.GL import GL_R32F, GL_RG32F, GL_RGB32F, GL_RGBA32F
from OpenGL.GL import GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST

from OpenGL.GL import GL_TEXTURE_COMPARE_MODE, GL_TEXTURE_COMPARE_FUNC
from OpenGL.GL import GL_COMPARE_REF_TO_TEXTURE, GL_LESS
from OpenGL.GL import GL_DEPTH_COMPONENT, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T
from OpenGL.GL import GL_REPEAT, GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_NONE
from OpenGL.GL import glBindFramebuffer, glDrawBuffer, glReadBuffer
from OpenGL.GL import glTexParameteri, glFramebufferTexture2D
from OpenGL.GL import glDetachShader, glGenFramebuffers

from OpenGL.arrays.vbo import VBO

from numpy import concatenate

from shaders import get_shader_path


def get_texture_type(dimensions):
    if dimensions == 1:
        return GL_TEXTURE_1D
    elif dimensions == 2:
        return GL_TEXTURE_2D
    elif dimensions == 3:
        return GL_TEXTURE_3D


def get_texture_constructor(dimensions):
    if dimensions == 1:
        return glTexImage1D
    elif dimensions == 2:
        return glTexImage2D
    elif dimensions == 3:
        return glTexImage3D


def get_color_internal_format(components):
    if components == 1:
        return GL_R32F
    elif components == 2:
        return GL_RG32F
    elif components == 3:
        return GL_RGB32F
    elif components == 4:
        return GL_RGBA32F


def get_color_format(components):
    if components == 1:
        return GL_RED
    elif components == 2:
        return GL_RG
    elif components == 3:
        return GL_RGB
    elif components == 4:
        return GL_RGBA


class ShadersHelper:
    """Helper class to work with program and shaders."""

    def __init__(self, vertex, fragment, number_of_buffers=0,
                 number_of_textures=0):
        """Initialize program with shaders."""
        self.__program = glCreateProgram()
        self.__current_shaders = {}
        self.__shaders = {
            GL_VERTEX_SHADER: [],
            GL_FRAGMENT_SHADER: []
        }
        self.__depth_map_fbo = None
        self.__attributes = []

        if not isinstance(vertex, list):
            vertex = [vertex]
        for v in vertex:
            self.__load_shader(get_shader_path(v), GL_VERTEX_SHADER)
        if not isinstance(fragment, list):
            fragment = [fragment]
        for f in fragment:
            self.__load_shader(get_shader_path(f), GL_FRAGMENT_SHADER)

        self.change_shader(0, 0)

        glLinkProgram(self.__program)
        assert glGetProgramiv(self.__program, GL_LINK_STATUS) == GL_TRUE

        self.__vao_id = glGenVertexArrays(1)
        glBindVertexArray(self.__vao_id)
        if number_of_buffers == 1:
            self.__vbo_id = [glGenBuffers(number_of_buffers)]
        elif number_of_buffers > 1:
            self.__vbo_id = glGenBuffers(number_of_buffers)

        if number_of_textures == 1:
            self.__textures_ids = [glGenTextures(1)]
        elif number_of_textures > 1:
            self.__textures_ids = glGenTextures(number_of_textures)
        self.__textures = []

    def change_shader(self, vertex=None, fragment=None):
        """Change vertex and fragment shader of current program.

        Needs indices of shaders from the list.
        """
        changed = False
        if vertex is not None:
            changed |= self.__attach_shader(
                self.__shaders[GL_VERTEX_SHADER][vertex], GL_VERTEX_SHADER)
        if fragment is not None:
            changed |= self.__attach_shader(
                self.__shaders[GL_FRAGMENT_SHADER][fragment],
                GL_FRAGMENT_SHADER)
        if not changed:
            return
        glLinkProgram(self.__program)
        assert glGetProgramiv(self.__program, GL_LINK_STATUS) == GL_TRUE

    def __attach_shader(self, shader_id, shader_type):
        """Attach the shader to the program."""
        if shader_type in self.__current_shaders:
            if self.__current_shaders[shader_type] == shader_id:
                return False
            glDetachShader(self.__program, self.__current_shaders[shader_type])
        self.__current_shaders[shader_type] = shader_id
        glAttachShader(self.__program, shader_id)
        return True

    def __load_shader(self, shader_filename, shader_type):
        """Load shader of specific type from file."""
        shader_source = ''
        with open(shader_filename) as shader_file:
            shader_source = shader_file.read()
            assert shader_source

        shader_id = glCreateShader(shader_type)
        self.__shaders[shader_type].append(shader_id)
        glShaderSource(shader_id, shader_source)
        glCompileShader(shader_id)

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

    def bind_uniform_vector(self, data, name):
        """Bind uniform vector parameter."""
        location = glGetUniformLocation(self.__program, name)
        assert location >= 0
        glUniform4f(location, *data.flatten())

    def bind_uniform_array(self, data, name):
        """Bind uniform array."""
        if data.dtype.kind == 'i':
            glUniformBinder = glUniform1iv
        elif data.dtype.kind == 'f':
            glUniformBinder = glUniform1fv
        location = glGetUniformLocation(self.__program, name)
        assert location >= 0
        glUniformBinder(location, data.size, data.flatten())

    def bind_buffer(self):
        """Prepare attributes and bind them."""
        VBO(concatenate(self.__attributes)).bind()

    def clear(self):
        """Unbind all bound entities and clear cache."""
        self.__attributes = []
        glUseProgram(0)
        glBindVertexArray(0)

    def bind_depth_texture(self, size):
        """Create depth texture for shadow map."""
        width, height = size
        texture_type = GL_TEXTURE_2D
        self.__depth_map_fbo = glGenFramebuffers(1)

        depth_map = self.__textures_ids[len(self.__textures)]
        glBindTexture(texture_type, depth_map)
        self.__textures.append(2)
        glTexImage2D(texture_type, 0, GL_DEPTH_COMPONENT,
                     width, height, 0, GL_DEPTH_COMPONENT,
                     GL_FLOAT, None)
        glTexParameteri(texture_type, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(texture_type, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(texture_type, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(texture_type, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE,
                        GL_COMPARE_REF_TO_TEXTURE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC,
                        GL_LESS)

        glBindFramebuffer(GL_FRAMEBUFFER, self.__depth_map_fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                               GL_TEXTURE_2D, depth_map, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind_texture(self, i):
        """Rebind texture for current program and shaders."""
        dimensions = self.__textures[i]
        if dimensions == 1:
            texture_type = GL_TEXTURE_1D
        elif dimensions == 2:
            texture_type = GL_TEXTURE_2D
        elif dimensions == 3:
            texture_type = GL_TEXTURE_3D
        glBindTexture(texture_type, self.__textures_ids[i])

    def bind_fbo(self):
        """Rebind depth map FBO for current program and shaders."""
        glBindFramebuffer(GL_FRAMEBUFFER, self.__depth_map_fbo)

    def create_float_texture(self, data, size, dimensions=2, components=3):
        """Bind texture with floating point vectors within.

        dimensions: dimensionality of the texture
                    vector, matrix, 3D matrix.
        components: dimensionality of texture element
                    number or 2D, 3D, 4D vector.
        """
        texture_type = get_texture_type(dimensions)
        texture_constructor = get_texture_constructor(dimensions)
        internal_format = get_color_internal_format(components)
        texture_format = get_color_format(components)

        glBindTexture(texture_type, self.__textures_ids[len(self.__textures)])
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # HACK: Python <3.5 doesn't allow to use *size
        # within enumerable arguments
        params = ([texture_type, 0, internal_format]
                  + list(size) + [0, texture_format, GL_FLOAT, data.flatten()])
        texture_constructor(*params)

        glTexParameterf(texture_type, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(texture_type, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.__textures.append(dimensions)

    def link_texture(self, name, number):
        """Link the texture to shaders."""
        location = glGetUniformLocation(self.__program, name)
        assert location >= 0
        glUniform1i(location, number)
