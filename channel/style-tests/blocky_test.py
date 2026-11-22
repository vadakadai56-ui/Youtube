"""Style test: blocky characters on the snowy night street (huss Short look)."""
import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline"))
import scene
scene.STYLE = os.environ.get("STYLE", "lowpoly")
from scene import *          # noqa
from world import street, cam
from characters import blocky, ball, dribble, stride
reset(); rng = random.Random(3)
street(rng)
kid = blocky((0.0, 0.0, 0), (0.85, 0.2, 0.2), pants=(0.15, 0.2, 0.35), style="kid", hat=(0.2, 0.55, 0.85), name="kid", rot=0.25)
b = ball((0, 0, 0.3)); stride(kid, 0.12, speed=0); dribble(kid, b, 0.18)
gran = blocky((-1.0, 0.9, 0), (0.62, 0.38, 0.6), pants=(0.3, 0.28, 0.35), style="gran", skin="tan", name="gran", rot=-0.4)
gran["L"].rotation_euler[1] = -2.4                    # waving
dad = blocky((1.05, 1.1, 0), (0.3, 0.5, 0.35), pants=(0.25, 0.22, 0.2), style="dad", skin="brown", name="dad", rot=0.5)
world_color((0.03, 0.04, 0.09)); light("AREA", (0.6, -2.0, 2.2), 45, col=(1.0, 0.85, 0.7), size=2.0, target=(0, 0, 0.6))
cam((0.25, -3.1, 1.0), (0.0, 0.4, 0.62), lens=32, fstop=3.5)
sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y = 1080, 1920; sc.render.resolution_percentage = 50
render(sys.argv[-1])
