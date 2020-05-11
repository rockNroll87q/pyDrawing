#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 12:36:27 2019

@author: Michele Svanera

University of Glasgow.

To run with PsychoPy 3 Coder.

"""


################################################################################################################
## Imports 

from __future__ import absolute_import, division, print_function


import glob
import pandas as pd
import numpy as np
from ast import literal_eval

from psychopy import visual, core, event
from PIL import Image


################################################################################################################
## Paths and Constants

Path_in = '../in/'
Path_in_csv = Path_in + 'csv/v2.0/'
Path_in_imgs = Path_in + 'images/'
Path_out = '../out/v2.0/'


Fullscreen = True
Screen_dimensions = (200,200)

Image_size = np.array((1.2, 0.9))


##############################################################################
## Functions


def normaliseVertexMatrix(array_vertices):
    
    return array_vertices / np.array([0.888888,0.5])


def convertListInNumpyTime(time_to_save):
    '''
    IN: list of list
    OUT: list (every image) of numpy 1-D
    '''
    all_times = []
    for i_image in time_to_save:
        
        # Check the list is empty
        str_all_times = i_image[1:-1]
        if str_all_times == '':
            all_times.append(np.zeros(1))            
        else:
            array_times = np.array([float(i_time) for i_time in (str_all_times.split(','))])
            all_times.append(np.array(array_times))
    
    return all_times


def convertListInNumpyVertices(vertex_to_save):
    '''
    IN: list of list
    OUT: list (every image) of numpy coordinates 2-D
    '''
    all_vertices = []
    
    # Check the list is empty
    if str(vertex_to_save[0]) == 'nan':
        return all_vertices

    for i_vertex in vertex_to_save:
        
        array_vertices = np.array(literal_eval(i_vertex))
        array_vertices = normaliseVertexMatrix(array_vertices)
        all_vertices.append(array_vertices.reshape(1,2))
    
    all_vertices = np.concatenate(all_vertices,axis=0)
    
    return all_vertices


def loadAndParseCsv(path_csv):
    '''
    IN:
        * path_csv [string]: path where all subject csvs are
    OUT:
        * all_data [list]:
            * list_of_images
            * vertex_to_save
            * time_to_save
            * participant_names
            * indeces_to_save    
    '''
    
    # Read every participants file
    all_csv = sorted(glob.glob(path_csv+'*.csv'))
    
    all_subjects_data = []
    
    # For every partecipant
    for c_csv_filename in all_csv:
        
        c_csv_filename_only = c_csv_filename.split('/')[-1]
        
        c_subj_data = {}
        # Read csv
        try:
            c_csv_file = pd.read_csv(c_csv_filename)

            c_subj_data['csv_filename'] = c_csv_filename_only                               # csv filename
            c_subj_data['img_name'] = c_csv_filename_only.split('#')[1]                     # Find image name
            c_subj_data['subj_name'] = c_csv_filename_only.split('_linedrawing_')[0]        # Find participant name

            c_subj_data['time_to_save'] = list(c_csv_file['time_to_save'])                  # Read times
            c_subj_data['indeces_to_save'] = list(c_csv_file['indeces_to_save'])            # Read indeces

            # Read vertex positions
            vertex_to_save = list(c_csv_file['vertex_to_save'])
            vertex_to_save = convertListInNumpyVertices(vertex_to_save)
            c_subj_data['vertex_to_save'] = vertex_to_save
            
        except:
            print('Impossible read (or parse) file: ' + c_csv_filename)
            
        all_subjects_data.append(c_subj_data)
        
    return all_subjects_data

       

################################################################################################################
## Main

# Now display every image and save the output in a file
    
def main_mouse(win,all_data):

    # For every image of every subject (for every file saved)
    for i_indx, i_file in enumerate(all_data):
        
        ############## Stimuli preparation ##############
        
        i_image = i_file['img_name']
        i_csv_filename = i_file['csv_filename']
        polygon_vertex = i_file['vertex_to_save']
        polygon_indx = np.array(i_file['indeces_to_save'])
        
        polygon_list = []

        if len(polygon_vertex) != 0:            # No drawings
            
            # I create N polygon based on how many were drawn
            for i in np.unique(polygon_indx):
                
                polygon_vertex_i = polygon_vertex[i == polygon_indx]
                
                polygon_list.append(visual.ShapeStim(win, vertices=polygon_vertex_i, closeShape=False,
                                                     fillColor=None, lineWidth=5, lineColor='black'))

        image = visual.ImageStim(win, image=Path_in_imgs+i_image, size=Image_size,
                                 units="height") #(1.0,1.0))
    
        ############## Definitions/Functions ##############
        
        ## handle Rkey presses each frame
        def escapeCondition():              
            for key in event.getKeys():
                if key in ['escape', 'q']:
                    return False
            return True

        ############## Exp. begin ##############
        
        break_flag = True
        globalClock = core.Clock()
        
        # To repeat at every image
        while 1:
            
            t = globalClock.getTime()
            if t > 0.1:
                break
            
            # Draw
            image.draw()
            if len(polygon_vertex) != 0:
                for i_pol in polygon_list:
                    i_pol.draw()
    
            win.flip()  # redraw the buffer                
    
            # Break conditions
            break_flag = escapeCondition()
            if break_flag == False:
                return

        ############## Exp. end ##############
        
        # Save frame
        last_frame_changed = np.array(win.getMovieFrame())
        last_frame_changed = Image.fromarray(last_frame_changed)#.convert('LA')
        out_filename = Path_out + i_csv_filename + '.png'
        print(out_filename)
        last_frame_changed.save(out_filename)
    
    
    # Display and Save occlusion only
    win.flip()
    occlusion = visual.Rect(win, pos=(Image_size[0]/4,-Image_size[1]/4), units="height",
                            size=Image_size, lineColor='black', fillColor='black')
    occlusion.draw()
    win.flip()
    
    occlusion_frame = np.array(win.getMovieFrame())
    occlusion_frame = Image.fromarray(occlusion_frame)#.convert('LA')
    occlusion_out_filename = Path_out + 'occlusion.png'
    occlusion_frame.save(occlusion_out_filename)
    
    return
 
    
    
if __name__ == "__main__":  

    all_subjects_data = loadAndParseCsv(Path_in_csv)
    
    # Start window
    win = visual.Window(Screen_dimensions, monitor="mon", units="norm", fullscr=Fullscreen,
                        color='white', allowGUI=False)
    win.recordFrameIntervals = True
    resX,resY = win.size
    
    # Main stimulation    
    try:
        main_mouse(win,all_subjects_data)
    except Exception as e:
        print(e)
    
    win.close()
    core.quit()





