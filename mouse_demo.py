#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Tue May  7 16:00:46 2019

@author: Michele Svanera

University of Glasgow.

Toy example on how to use the mouse to draw stuff
 
"""

################################################################################################################
## Imports 

from __future__ import absolute_import, division, print_function


from psychopy import visual, core, event
from psychopy.iohub import launchHubServer


################################################################################################################
## Paths and Constants

Fullscreen = False
Screen_dimensions = (1000,1000)

Empty_shapes = 100


################################################################################################################
## Functions


def main_mouse(win):

    ############## Stimuli preparation ##############

    # Create some psychopy visual stim (same as how you would do so normally):
    mouse_cursor = visual.GratingStim(win, tex="none", mask="gauss",
        pos=(0, 0), size=(30, 30), color='black', autoLog=False)
    
    
    polygon_vertex = [(0,0)]
    polygon_list = []
    for i in range(Empty_shapes):
        polygon_list.append(visual.ShapeStim(win, vertices=polygon_vertex, 
                                             fillColor=None, lineWidth=5, lineColor='black'))


    ############## Definitions/Functions ##############
    
    ## handle Rkey presses each frame
    def escapeCondition():              
        for key in event.getKeys():
            if key in ['escape', 'q']:
                return False
        return True
    

    ############## Init mouse ##############
    
    # create the process that will run in the background polling devices
    mouse = event.Mouse(visible=False, win=win)  #  will use win by default
    

    ############## Exp. begin ##############
    
    first_iteration = True
    indx_shape = 0      # How many I draw so far
    before_left_button = False
    break_flag = True
    
    while break_flag:
        
        # I work on this trace
        polygon = polygon_list[indx_shape]
        
        # Get the current mouse position and state
        mouse_position = mouse.getPos()
        left_button, middle_button, right_button = mouse.getPressed()
        
        # If the left button is pressed, start drawing
        if left_button:
            
            # Initialise polygon_vertex
            if first_iteration == True:
                polygon_vertex = []
                first_iteration = False
                before_left_button = True
            
            # Update 
            polygon_vertex.append(mouse_position)
            polygon.vertices = polygon_vertex

        else:
            # Did the partecipant stop drawing?
            if before_left_button:                
                before_left_button = False
                first_iteration = True
                indx_shape += 1 
    

        # Display on screen
        mouse_cursor.setPos(mouse_position)
        mouse_cursor.draw()
        
        for i_pol in range(indx_shape+1):
            polygon_list[i_pol].draw()

        win.flip()  # redraw the buffer                

        # Break conditions
        break_flag = escapeCondition()
        if indx_shape >= (Empty_shapes-1):
            break_flag = False


    return



if __name__ == "__main__":  

    # Start window
    win = visual.Window(Screen_dimensions, monitor="mon", units="pix", fullscr=Fullscreen,
                        color='white', allowGUI=False)
    win.recordFrameIntervals = True
    resX,resY = win.size

    # Main stimulation    
    try:
        main_mouse(win)
    except Exception as e:
        print(e)
    
    win.close()
    core.quit()


