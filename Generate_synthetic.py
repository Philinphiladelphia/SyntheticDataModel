import os
import numpy as np 
import math
import sys
import subprocess
import random
#fixed point camera, point light and object rotation change

#8 light points,  rotations


#arguments should be, blender_file_directory, number of generated images, output='verbose'

if len(sys.argv) > 5:
    raise TypeError('Expected at most 5 arguments, recieved {}'.format(len(sys.argv)))

#necessary values to pass to object





light_tuples = []
light_hues = []

#given in wattages,
#LED: 
light_intensity = []

#array of possible x,y,z rotations to place object at
object_rotations = []
radius = 1
#create 8 evenly spaced out points on circle and rotations pointing at home


for i in range(0,8):
    i = i/4
    for j in range (0,8):
        j = j/4
        for k in range(0,8):
            k = k/4
            obj_rotation = [(math.pi *i), (math.pi * j), (math.pi * k)]
            object_rotations.append(obj_rotation)

print(object_rotations)

random.shuffle(object_rotations)



for i in range(0,8):
    temp_loc = [0,0,0]
    i = i/4 
    temp_loc[0] = radius * np.cos(i)
    temp_loc[1] = radius * np.sin(i)
    temp_loc[2] = 1
    light_rot = [(i*math.pi),0,(i+1)*math.pi]
    light_tuples.append([temp_loc,light_rot])

random.shuffle(light_tuples)


#use 

#obj_filepath = '/Users/gavinfox/thisis/a/testfilepath.blend'
#bj_rot = '15, 33, 42'
#ight_loc = '1,0,1'
#light_rot = '3.765, 0, 3.4512'
#ight_intense = '100' 



#5: object file path 
#6: object rotation
#7: light location
#8: light rotation
#9: light intensity
#10: output file path
#11: iter_num
#objecti = [(math.pi/2),0,0]
#light_location = [1,0,1]
#ight_rot = [0,0, (math.pi/4)]
#ight_intense = '1000'
#output_path = '/Users/gavinfox/Documents/Blender_output_imgs/image'
#iter_num = str(1)
#obj_filepath = '/Users/gavinfox/Downloads/uploads_files_2114252_redyellow-apple-textured-for-eevee-and-cycles.blend'
#obj_filepath = '/Users/gavinfox/Downloads/uploads_files_2656985_Coke+Can.blend'
#obj_filepath = '/Users/gavinfox/Downloads/uploads_files_2868947_SMK_JJ0KQAO2_Watermelon_2.91.blend'
#light_loc = str(light_location[0])+','+str(light_location[1])+','+str(light_location[2]) 
#light_rot = str(light_rot[0])+','+str(light_rot[1])+','+str(light_rot[2]) 



#!blender temp_blend.blend --background --python Scene_creation.py 

for i in range(0,512):
    output_path = '/Users/gavinfox/Documents/Blender_output_imgs/image'
    obj_filepath = '/Users/gavinfox/Downloads/uploads_files_2114252_redyellow-apple-textured-for-eevee-and-cycles.blend'
    light_intense = '1000'

    objecti = object_rotations[i]
    light_iter = random.randint(0,7)
    light_location = light_tuples[light_iter][0]
    light_rot = light_tuples[light_iter][1]
    
    obj_rot = str(objecti[0])+','+str(objecti[1])+','+str(objecti[2]) 
    light_loc = str(light_location[0])+','+str(light_location[1])+','+str(light_location[2]) 
    light_rot = str(light_rot[0])+','+str(light_rot[1])+','+str(light_rot[2]) 
    iter_num = str(i)
    print('Running subprocess', i)
    process = subprocess.run(['/Applications/Blender.app/Contents/MacOS/blender',
    '/Users/gavinfox/temp_blend.blend',
    '--background', 
    '--python',
    '/Users/gavinfox/Scene_creation_final.py',
    obj_filepath,
    obj_rot,
    light_loc,
    light_rot,
    light_intense,
    output_path,
    iter_num], universal_newlines=True)

    print('Subprocess completed', i)