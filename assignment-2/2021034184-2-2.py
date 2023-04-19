#!/usr/bin/env python3

import glfw
from OpenGL.GL import *
import numpy as np


#Adapting code from class 2 given by professor 이윤상

def render(option):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(option)
    for i in range(0, 360, 30):
    	glVertex2f(np.cos(np.deg2rad(i)), np.sin(np.deg2rad(i)))
    
    glEnd()

def main(option):
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2021034184-2-2", None,None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render(option)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    index = input("Insert the type number: ")
    types = [GL_POLYGON, GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP]
    option = types[int(index)]
    main(option)
	

