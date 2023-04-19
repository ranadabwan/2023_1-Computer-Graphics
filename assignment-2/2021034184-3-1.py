#!/usr/bin/env python3

import time
import glfw
from OpenGL.GL import *
import numpy as np


#Adapting code from class 2 given by professor 이윤상

def render(T):
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()
	# draw cooridnate
	glBegin(GL_LINES)
	glColor3ub(255, 0, 0)
	glVertex2fv(np.array([0.,0.]))
	glVertex2fv(np.array([1.,0.]))
	glColor3ub(0, 255, 0)
	glVertex2fv(np.array([0.,0.]))
	glVertex2fv(np.array([0.,1.]))
	glEnd()
	# draw triangle
	glBegin(GL_TRIANGLES)
	glColor3ub(255,255,255)
	glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
	glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
	glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1])
	glEnd()

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2021034184-3-1", None,None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    
    glfw.swap_interval(1)
    angle = 0

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        
        if angle > 360:
        	angle = 0
        	
        	
        #t = glfw.get_time()
        t = np.deg2rad(angle)
        s = np.sin(t)
        c = np.cos(t)
        #first two for rotaion and last for translation
        T = np.array([[c,-s,0.5*c],[s,c,0.5*s], [0,0,1]]) 

        # Render here, e.g. using pyOpenGL
        render(T)
        angle = angle + 30

        # Swap front and back buffers
        glfw.swap_buffers(window)
        time.sleep(0.0850)
    glfw.terminate()

if __name__ == "__main__":
	main()

