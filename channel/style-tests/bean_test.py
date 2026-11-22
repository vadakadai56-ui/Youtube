import os, sys, random
sys.path.insert(0, "/home/user/youtube/pipeline")
import scene; scene.STYLE = "lowpoly"
from scene import *
from world import kitchen, cam
from characters import bean
reset(); kitchen(random.Random(2))
a = bean((-0.45, 0.2, 0), (0.35, 0.65, 0.95), name="you", tuft=(0.25, 0.15, 0.1), rot=0.2)
b = bean((0.05, 0.35, 0), (0.98, 0.6, 0.35), name="friend", mouth="open", bow=(0.9, 0.2, 0.3), rot=-0.1)
g = bean((0.55, 0.3, 0), (0.75, 0.55, 0.85), name="gran", style="gran", rot=-0.3)
a["R"].rotation_euler[1] = -2.4
light("AREA", (0, -2.2, 2.0), 120, col=(1, 0.95, 0.9), size=2.5, target=(0, 0.3, 0.5))
cam((0.05, -1.9, 0.75), (0.05, 0.3, 0.5), lens=34, fstop=3.5)
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = 40
render(sys.argv[-1])
