#include <GLFW/glfw3.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

int status = -1;
float rotation[] = {0.f, 0.f, 0.f};
int forward_rotation_keys[] = {GLFW_KEY_DOWN, GLFW_KEY_LEFT, GLFW_KEY_Z};
int back_rotation_keys[] = {GLFW_KEY_UP, GLFW_KEY_RIGHT, GLFW_KEY_A};

static void error_callback(int error, const char* description) {
    fputs(description, stderr);
}

static void key_callback(GLFWwindow* window, int key, int scancode,
                                             int action, int mods)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GL_TRUE);
        status = 1;
    } else if (key == GLFW_KEY_Q && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GL_TRUE);
        status = 0;
    } else if (key == GLFW_KEY_N && action == GLFW_PRESS) {
        glfwSetWindowShouldClose(window, GL_TRUE);
        status = 2;
    }

    int i = 0;
    do {
        if (key == forward_rotation_keys[i] && action != GLFW_RELEASE) {
            rotation[i] = 1.f;
        } else if (key == back_rotation_keys[i] && action != GLFW_RELEASE) {
            rotation[i] = -1.f;
        } else if (key == back_rotation_keys[i]
                || key == forward_rotation_keys[i]) {
            rotation[i] = 0.f;
        }
    } while (++i < sizeof(rotation) / sizeof(*rotation));
}

int render_face(float* vertices, float* colors,
                 uint16_t* triangles, int amount) {
    GLFWwindow* window;
    glfwSetErrorCallback(error_callback);

    if (!glfwInit()) {
        exit(EXIT_FAILURE);
    }

    window = glfwCreateWindow(640, 480, "Simple example", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);
    glfwSetKeyCallback(window, key_callback);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glOrtho(-1.5f, 1.5f, -1.5f, 1.5f, -1.5f, 1.5f);
    glEnable(GL_DEPTH_TEST);
    glDepthMask(GL_TRUE);

    while (!glfwWindowShouldClose(window))
    {
        float ratio;
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        ratio = width / (float) height;
        glViewport(0, 0, width, height);

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glClearColor(1.f, 1.f, 1.f, 0.f);

        glRotatef(1.f, rotation[0], rotation[1], rotation[2]);
        glBegin(GL_TRIANGLES);
        size_t i = 0;
        unsigned short j = 0;
        float r, g, b;
        while (i < amount) {
            j = triangles[i];
            r = colors[3*j];
            g = colors[3*j+1];
            b = colors[3*j+2];
            glColor3f(r, g, b);
            glVertex3f(vertices[3*j], vertices[3*j+1], vertices[3*j+2]);
            i++;
        }
        glEnd();
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwDestroyWindow(window);
    glfwTerminate();
    return status;
}

