import bpy
import mathutils
import os
import sys
from time import time
import math
import numpy as np
from math import radians as radians
import json


def configure_render(mesh_y_dim, output_filepath, iter_val):
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.filepath = output_filepath + str(iter_val) + '/Image/Image0001'

        #Output open exr .exr files
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        bpy.context.scene.cycles.samples = 50

        # Configure renderer to record object index
        bpy.context.scene.view_layers["View Layer"].use_pass_object_index = True

        # Switch on nodes and get reference
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        links = tree.links

        ## Clear default nodes
        for node in tree.nodes:
           tree.nodes.remove(node)

        # Create a node for outputting the rendered image
        image_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
        image_output_node.label = "Image_Output"
        image_output_node.base_path = output_filepath +str(iter_val) +'/Image'
        image_output_node.location = 400,0

        # Create a node for outputting the depth of each pixel from the camera
        depth_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
        depth_output_node.label = "Depth_Output"
        depth_output_node.base_path = output_filepath + str(iter_val)+ '/Depth'
        depth_output_node.location = 400,-100

        # Create a node for outputting the index of each object
        index_output_node = tree.nodes.new(type="CompositorNodeOutputFile")
        index_output_node.label = "Index_Output"
        index_output_node.base_path = output_filepath + str(iter_val) + '/Segment'
        index_output_node.location = 400,-200

        # Create a node for the output from the renderer
        render_layers_node = tree.nodes.new(type="CompositorNodeRLayers")
        render_layers_node.location = 0,0

        #create Map Range node
        map = tree.nodes.new(type='CompositorNodeMapRange')
        #TODO: change default values based on dimensions of object being passed in
        map.inputs[1].default_value = 1 - (mesh_y_dim)
        map.inputs[2].default_value = 1 + (mesh_y_dim)
        map.inputs[4].default_value = 1
        map.location = 250,-400
        links.new(render_layers_node.outputs['Depth'], map.inputs['Value'])
        links.new(map.outputs['Value'], depth_output_node.inputs['Image'])
    
        # Link all the nodes together
        links.new(render_layers_node.outputs['Image'], image_output_node.inputs['Image'])
    #    links.new(render_layers_node.outputs['Depth'], depth_output_node.inputs['Image'])
        links.new(render_layers_node.outputs['IndexOB'], index_output_node.inputs['Image'])


#5: object file path 
#6: object rotation
#7: light location
#8: light rotation
#9: light intensity
#10: output file path
#11: iter num
print("PASSED ARGUMENTS")
for each in sys.argv:
    print(each)



obj_rotation = sys.argv[6].split(',')
print

for i in range(0,len(obj_rotation)):
    obj_rotation[i] = float(obj_rotation[i])
    
light_loc = sys.argv[7].split(',')
for i in range(0,len(light_loc)):
    light_loc[i] = float(light_loc[i])
    
light_rot = sys.argv[8].split(',')
for i in range(0,len(light_rot)):
    light_rot[i] = float(light_rot[i])
    
iter_val = int(sys.argv[11])

    

start_time = time()

path = os.getcwd()
print(path)



scene = bpy.context.scene
print(scene.collection.objects)

for obj in bpy.data.objects:
    print(obj.name)

print(bpy.data.scenes)

print(bpy.data.scenes.keys())


#Remove all meshes currently in scene

for each in bpy.data.meshes:
    print(each.name)
    bpy.data.meshes.remove(each)


#if "Cube" in bpy.data.meshes:
#    mesh = bpy.data.meshes["Cube"]
#   print(mesh)
#   bpy.data.meshes.remove(mesh)

#print(bpy.data.objects['Camera'].location)
#print(bpy.data.objects['Light'].location)

#create a scene
#scene = bpy.data.scenes.new('Scene')
#scene = bpy.context.scene
#create a camera
#camera_data = bpy.data.cameras.new('Camera')

#camera = bpy.data.objects.new('Camera', camera_data)
#camera.location = (-2.0, 3.0, 3.0)
#camera.rotation_euler = ([radians(a) for a in (422.0, 0.0, 149)
#scene.collection.objects.link(camera)

#create lamp
#light_data = bpy.data.lamps.new('light',type='POINT')
#light = bpy.data.objects.new('light',light_data)
#scene.collection.objects.link(light)
#light.location = mathutils.Euler((0.9, 0.0, 1.1))

#scene.update()


#append object from another blend file

#for each in os.listdir("/Users/gavinfox/append_test.blend\\Object\\"):
#    print(each)

#file_path = "/Users/gavinfox/apend_test.blend"
#inner_path = "Object"
#object_name = "Icosphere"
 
#bpy.ops.wm.append(
#    filepath=os.path.join(file_path, inner_path, object_name),
#    filename=object_name,
#    directory=os.path.join(file_path, inner_path)
#   )
#bpy.ops.wm.append(
#    directory = "/Users/gavinfox/append_test.blend\\Object\\",
#    filename = "Icosphere"
#   )


#TODO: Make this code work so that any meshes contained within loaded file are able to be added to the scene,
#rather than having to know the specific 

#apple_test_file = '/Users/gavinfox/Downloads/uploads_files_2114252_redyellow-apple-textured-for-eevee-and-cycles.blend'

obj_blend_filepath = sys.argv[5]


with bpy.data.libraries.load(obj_blend_filepath) as (data_from, data_to):
    data_to.objects = [name for name in data_from.objects]
    
for each in data_to.objects:
    print(each,each.type)
    if each.type == 'MESH':
       #scene.collection.objects.link(each)
       bpy.data.collections['Collection'].objects.link(each)
       



#TODO: Based on dimensions of passed object, adjust scale to fit specific ratio
for each in bpy.data.objects:
    if each.type == 'MESH':
        #each.rotation_euler = ((math.pi/2),(math.pi/2),0)
        each.rotation_euler = (obj_rotation[0], obj_rotation[1], obj_rotation[2])
        print('PRE_SCALE_DIMS',each.dimensions)
        object_dims = each.dimensions
        #each.scale = (20,20,20)
        each.pass_index = 14
        #print('MATERIAL',each.active_material, len(each.material_slots))
        #print('PASS_INDEX', each.pass_index)
    print(each.name, each.type)
    print('LOCATION',each.location)
    print('ROTATION',each.rotation_euler)
    if each.type == 'LIGHT':
        each.location= (light_loc[0],light_loc[1],light_loc[2])
        each.rotation_euler = (light_rot[0],light_rot[1],light_rot[2])
        #each.power = int(sys.argv[9])
    
bpy.context.scene.camera = bpy.data.objects['Camera']
bpy.context.scene.camera.location = (0, -(1+object_dims[1]),0)
bpy.context.scene.camera.rotation_euler = ((math.pi/2),0,0)

configure_render(object_dims[1], sys.argv[10], iter_val)


#TODO: up the light path tracing for complete render

bpy.ops.render.render(write_still = True)

data = {}
data['obj_filepath'] = sys.argv[5]
data['obj_rot'] = obj_rotation
data['light_loc'] = light_loc
data['light_rot'] = light_rot
data['light_intensity'] = int(sys.argv[9])
data['iter_num'] = iter_val

with open((sys.argv[10] + '{}/data.json'.format(iter_val)), 'w') as outfile:
    json.dump(data, outfile) 

end_time = time()
print('Code completed in', (end_time - start_time))

