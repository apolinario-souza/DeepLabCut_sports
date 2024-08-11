# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 09:04:12 2023

@author: Tércio Apolinário-Souza. edf.tercio@gmail.com
"""

import deeplabcut

# 1. "Please specify the directory where the files will be saved. 
# Adjust the '/' in the path accordingly."
main_path = "C:/Users/edfte/OneDrive/Documentos/Tutorial/" 

#2. Define the names for your project
name_project = "Game"
name_experimenter = "hand"
data = '2024-08-11'

#3. Enter the address in the analyzed video. Adjust the '/' direction as needed.
path_video = "C:/Users/edfte/OneDrive/Documentos/Tutorial/videos/hand.mp4"




#       DO NOT MAKE ANY CHANGES TO THE SCRIPT FROM THIS POINT FORWARD #####


path_save = main_path


deeplabcut.create_new_project(name_project, name_experimenter, [path_video], working_directory=path_save, copy_videos=True, multianimal=False)

input("CHANGE FILE config.yaml and Press Enter to continue...")
      

config_path = path_save +name_project+'-'+name_experimenter+ '-'+data+'/config.yaml'
      
deeplabcut.extract_frames(config_path, mode='automatic', algo='kmeans', userfeedback=False, crop=False)


input("Press Enter to continue...")
      
      
deeplabcut.label_frames(config_path)
input("Press Enter to continue...")
      
deeplabcut.check_labels(config_path, visualizeindividuals=True)
deeplabcut.create_training_dataset(config_path, augmenter_type='imgaug')


