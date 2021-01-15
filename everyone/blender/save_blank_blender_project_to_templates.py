#!/usr/bin/env python
import os
import bpy

# profile = os.environ.get("HOME")
# sources = os.path.join(profile, ".local/share/templates/.source")
# source = os.path.join(sources, "blender_project.blend")
source = os.path.join("/tmp", "blender_project.blend")

# bpy.ops.mesh.select_all(action='SELECT')
# ^
# Traceback (most recent call last):
#  File "/home/owner/git/linux-preinstall/everyone/blender/save_blank_blender_project_to_templates.py", line 9, in <module>
#    bpy.ops.mesh.select_all(action='SELECT')
#  File "/usr/share/blender/2.91/scripts/modules/bpy/ops.py", line 132, in __call__
#    ret = _op_call(self.idname_py(), None, kw)
#RuntimeError: Operator bpy.ops.mesh.select_all.poll() failed, context is incorrect
# (THAT IS FOR EDIT MODE)

bpy.ops.object.select_all(action='SELECT')


if len(bpy.context.selected_objects) > 0:
# if len(bpy.data.objects) > 0:
    for obj in bpy.context.selected_objects:
    # for obj in bpy.data.objects:
        print(obj.name, obj, obj.type)
        if obj.name != 'Cube':
            try:
                # bpy.data.objects[obj.name].select_set(False)
                obj.select_set(False)
            except AttributeError:
                # 2.7x
                obj.select = False

bpy.ops.object.delete()


# bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
bpy.ops.wm.save_as_mainfile(filepath=source)
