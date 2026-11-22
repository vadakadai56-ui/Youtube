import os, sys, random
sys.path.insert(0, "/home/user/youtube/pipeline")
import scene; scene.STYLE = ""
from scene import *
from world import street, cam
from characters import clay
reset(); street(random.Random(5)); world_color((0.05, 0.06, 0.12))
a = clay((-0.4, 0.0, 0), (0.85, 0.3, 0.25), name="kid", style="kid", hat=(0.25, 0.5, 0.85), scarf=(0.95, 0.85, 0.3))
b = clay((0.0, 0.2, 0), (0.35, 0.45, 0.6), name="abel", style="old", glasses=True, rot=-0.2)
c = clay((0.42, 0.05, 0), (0.95, 0.75, 0.35), name="gran", style="adult", hair=(0.6, 0.35, 0.2), rot=-0.4, mouth="open")
a["R"].rotation_euler[1] = -2.4
light("AREA", (0.4, -2.0, 1.8), 60, col=(1, 0.85, 0.7), size=2.0, target=(0, 0, 0.5))
cam((0.05, -1.9, 0.65), (0, 0.1, 0.5), lens=36, fstop=3.0)
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = 40
render(sys.argv[-1])
