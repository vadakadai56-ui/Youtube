"""Dustlight 3D toolkit (Blender bpy): materials, primitives, lights, camera, the Lost Toy Room set, toys and Bun-Bun.

Import from story scripts:  from scene import *
Environment knobs: SAMPLES (Cycles samples), PCT (render % of 1080x1920), ENGINE (CYCLES|EEVEE), ES (Eevee samples).
"""
import bpy, math, os, random
from mathutils import Vector, Euler

RES = (1080, 1920)
SAMPLES = int(os.environ.get("SAMPLES", "40"))
SCALE = int(os.environ.get("PCT", "50"))
ENGINE = os.environ.get("ENGINE", "CYCLES").upper()
ES = int(os.environ.get("ES", "12"))
MATS = {}


# ---------------------------------------------------------------- scene setup
def reset(engine=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MATS.clear()
    sc = bpy.context.scene
    eng = (engine or ENGINE).upper()
    if eng == "EEVEE":
        sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = ES
    else:
        sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SAMPLES
        sc.cycles.use_denoising = True; sc.cycles.max_bounces = 6
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.resolution_percentage = SCALE
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.010, 0.02, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    return sc


def world_color(rgb):
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (*rgb, 1)


STYLE = os.environ.get("STYLE", "")


def lowpoly_pass(ratio=0.18, min_size=0.06):
    """Faceted low-poly look: flat shading plus a Decimate on every mesh bigger than min_size (eyes and tiny details stay smooth)."""
    for o in bpy.data.objects:
        if o.type != "MESH" or "lowpoly" in o: continue
        o["lowpoly"] = 1
        if max(o.dimensions) < min_size or len(o.data.polygons) < 40: continue
        for p in o.data.polygons: p.use_smooth = False
        d = o.modifiers.new("lp", "DECIMATE"); d.decimate_type = "COLLAPSE"; d.ratio = ratio; d.use_collapse_triangulate = True


LOOK = os.environ.get("LOOK", "")


def render(path):
    if STYLE == "lowpoly": lowpoly_pass()
    if LOOK and not bpy.context.scene.get("look_done"): apply_look(LOOK); bpy.context.scene["look_done"] = 1
    bpy.context.view_layer.update()
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


# ---------------------------------------------------------------- materials
def mat(name, col, rough=0.6, sheen=0.0, metal=0.0, emit=None, emit_str=0.0, noise=0.0, coat=0.0, alpha=1.0):
    key = (name, col, rough, sheen, metal, emit, emit_str, noise, coat, alpha)
    if key in MATS: return MATS[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if sheen: b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Sheen Roughness"].default_value = 0.6
    if coat: b.inputs["Coat Weight"].default_value = coat
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        if hasattr(m, "surface_render_method"): m.surface_render_method = "BLENDED"
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = emit_str
    if noise:                                       # fabric / wood mottling
        tex = nt.nodes.new("ShaderNodeTexNoise"); tex.inputs["Scale"].default_value = 60; tex.inputs["Detail"].default_value = 8
        mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.inputs["Factor"].default_value = noise
        mix.inputs[6].default_value = (*col, 1); mix.inputs[7].default_value = (col[0] * 0.6, col[1] * 0.6, col[2] * 0.6, 1)
        nt.links.new(tex.outputs["Fac"], mix.inputs["Factor"])
        nt.links.new(mix.outputs[2], b.inputs["Base Color"])
        bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.15
        nt.links.new(tex.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    MATS[key] = m
    return m


def bsdf(m):
    return m.node_tree.nodes["Principled BSDF"]


def set_color(m, col):
    """Recolour a material made by mat(), including its noise mottling."""
    b = bsdf(m); b.inputs["Base Color"].default_value = (*col, 1)
    for n in m.node_tree.nodes:
        if n.type == "MIX" and getattr(n, "data_type", "") == "RGBA":
            n.inputs[6].default_value = (*col, 1); n.inputs[7].default_value = (col[0] * 0.6, col[1] * 0.6, col[2] * 0.6, 1)


LOOKS = {   # per-video grade, picked in the story's style recipe (owner: videos must not all look the same)
    "story":  dict(view="AgX", look="AgX - Medium High Contrast", exposure=0.0, sat=1.0),
    "comedy": dict(view="Standard", look="Medium High Contrast", exposure=-0.9, sat=1.3),
    "horror": dict(view="AgX", look="AgX - High Contrast", exposure=-0.3, sat=0.8),
    "dream":  dict(view="Standard", look="Medium Contrast", exposure=-0.7, sat=1.3),
}


def apply_look(name):
    """Set the colour transform, contrast, exposure and a saturation boost for the whole scene (call after the set is built)."""
    L = LOOKS.get(name or "story", LOOKS["story"]); sc = bpy.context.scene
    sc.view_settings.view_transform = L["view"]; sc.view_settings.look = L["look"]; sc.view_settings.exposure = L["exposure"]
    if L["sat"] != 1.0:
        for m in bpy.data.materials:
            if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes: continue
            c = bsdf(m).inputs["Base Color"].default_value; mx, mn = max(c[:3]), min(c[:3])
            if mx - mn > 0.04:
                set_color(m, tuple(min(1.0, max(0.0, mn + (v - mn) * L["sat"])) for v in c[:3]))


# ---------------------------------------------------------------- primitives
def _finish(o, m=None, smooth=True, bevel=0.0):
    if m: o.data.materials.append(m)
    if smooth and o.type == "MESH":
        for p in o.data.polygons: p.use_smooth = True
    if bevel:
        bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = 3
    return o


def cube(loc, size, m, rot=(0, 0, 0), bevel=0.0, name="cube"):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    return _finish(o, m, smooth=False, bevel=bevel)


def sphere(loc, r, m, scale=(1, 1, 1), rot=(0, 0, 0), name="sph", seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r, rotation=rot, segments=seg, ring_count=seg // 2)
    o = bpy.context.object; o.name = name; o.scale = scale
    return _finish(o, m)


def cyl(loc, r, depth, m, rot=(0, 0, 0), name="cyl", verts=32, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=depth, rotation=rot, vertices=verts)
    o = bpy.context.object; o.name = name
    return _finish(o, m, bevel=bevel)


def torus(loc, major, minor, m, rot=(0, 0, 0), name="torus"):
    bpy.ops.mesh.primitive_torus_add(location=loc, rotation=rot, major_radius=major, minor_radius=minor)
    o = bpy.context.object; o.name = name
    return _finish(o, m)


def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(e); e.location = loc
    return e


def group(name, objs, parent_loc=(0, 0, 0)):
    """Parent objects (built at world coords) to a new empty at parent_loc, keeping their placement."""
    e = empty(name, parent_loc)
    for o in objs:
        o.parent = e; o.location = Vector(o.location) - Vector(parent_loc)
    return e


def text(body, loc, size, m, rot=(math.pi / 2, 0, 0), align="CENTER", extrude=0.002, name="txt"):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.body = body; o.data.size = size
    o.data.align_x = align; o.data.align_y = "CENTER"; o.data.extrude = extrude
    o.data.materials.append(m)
    return o


def hide(o, flag=True):
    for c in [o] + list(o.children_recursive): c.hide_render = flag


# ---------------------------------------------------------------- camera & lights
def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(loc, target, lens=35, dof=None, fstop=2.8):
    cd = bpy.data.cameras.new("cam"); cd.lens = lens
    c = bpy.data.objects.new("cam", cd); bpy.context.collection.objects.link(c)
    c.location = loc; look_at(c, target); bpy.context.scene.camera = c
    if dof:
        cd.dof.use_dof = True; cd.dof.focus_distance = dof; cd.dof.aperture_fstop = fstop
    return c


def light(kind, loc, energy, col=(1, 0.8, 0.6), size=0.2, rot=None, target=None, spot=None):
    ld = bpy.data.lights.new("l", kind); ld.energy = energy; ld.color = col
    if kind in ("POINT", "SPOT"): ld.shadow_soft_size = size
    if kind == "AREA": ld.size = size
    if kind == "SPOT" and spot: ld.spot_size = spot; ld.spot_blend = 0.6
    o = bpy.data.objects.new("l", ld); bpy.context.collection.objects.link(o); o.location = loc
    if rot: o.rotation_euler = rot
    if target: look_at(o, target)
    return o


# ---------------------------------------------------------------- palette
WOOD = (0.32, 0.17, 0.08); WOOD_D = (0.16, 0.08, 0.04); WALL = (0.30, 0.22, 0.16); FLOOR = (0.22, 0.12, 0.06)
FUR = (0.78, 0.66, 0.52); FUR_D = (0.55, 0.44, 0.33); PINK = (0.85, 0.42, 0.45); BLACK = (0.01, 0.01, 0.012)
TOYC = [(0.80, 0.12, 0.10), (0.10, 0.35, 0.80), (0.95, 0.70, 0.08), (0.12, 0.60, 0.25), (0.85, 0.40, 0.70), (0.95, 0.45, 0.10), (0.35, 0.20, 0.70)]


# ---------------------------------------------------------------- toys
def toy_block(loc, s, rng):
    o = cube(loc, (s, s, s), mat("blk", rng.choice(TOYC), 0.5, noise=0.15), rot=(0, 0, rng.uniform(-0.5, 0.5)), bevel=s * 0.12, name="block")
    t = text(rng.choice("ABCXYZ123"), (0, 0, 0), s * 0.7, mat("ink", (0.95, 0.92, 0.85), 0.5), name="letter")
    t.parent = o; t.location = (0, -s / 2 - 0.002, -s * 0.22); t.rotation_euler = (math.pi / 2, 0, 0)
    return o


def toy_ball(loc, r, rng):
    return sphere((loc[0], loc[1], loc[2] + r), r, mat("ball", rng.choice(TOYC), 0.25, coat=0.5), name="ball")


def toy_car(loc, s, rng):
    m = mat("car", rng.choice(TOYC), 0.25, coat=0.7); tm = mat("tyre", (0.03, 0.03, 0.03), 0.8)
    parts = [cube((loc[0], loc[1], loc[2] + s * 0.35), (s * 1.8, s * 0.9, s * 0.45), m, bevel=s * 0.15),
             cube((loc[0] - s * 0.1, loc[1], loc[2] + s * 0.72), (s * 0.95, s * 0.8, s * 0.4), m, bevel=s * 0.15)]
    for dx in (-0.6, 0.6):
        for dy in (-0.45, 0.45):
            parts.append(cyl((loc[0] + dx * s, loc[1] + dy * s, loc[2] + s * 0.2), s * 0.22, s * 0.15, tm, rot=(math.pi / 2, 0, 0)))
    g = group("car", parts, loc); g.rotation_euler[2] = rng.uniform(-0.6, 0.6)
    return g


def toy_duck(loc, s):
    m = mat("duck", (0.98, 0.78, 0.05), 0.3, coat=0.6); bm = mat("beak", (0.95, 0.35, 0.05), 0.4)
    parts = [sphere((loc[0], loc[1], loc[2] + s * 0.45), s * 0.55, m, scale=(1.2, 0.9, 0.8)),
             sphere((loc[0] + s * 0.35, loc[1], loc[2] + s * 0.95), s * 0.33, m),
             sphere((loc[0] + s * 0.68, loc[1], loc[2] + s * 0.92), s * 0.13, bm, scale=(1.4, 1, 0.6))]
    for dy in (-0.14, 0.14):
        parts.append(sphere((loc[0] + s * 0.55, loc[1] + dy * s, loc[2] + s * 1.05), s * 0.05, mat("eye", BLACK, 0.2)))
    return group("duck", parts, loc)


def toy_teddy(loc, s, col, worn=0.3):
    m = mat("ted", col, 0.9, sheen=0.8, noise=worn); md = mat("tedd", tuple(c * 0.7 for c in col), 0.9, sheen=0.8)
    e = mat("bead", BLACK, 0.15)
    parts = [sphere((loc[0], loc[1], loc[2] + s * 0.5), s * 0.5, m, scale=(1, 0.85, 1.1)),
             sphere((loc[0], loc[1], loc[2] + s * 1.25), s * 0.38, m),
             sphere((loc[0], loc[1] - s * 0.3, loc[2] + s * 1.17), s * 0.15, md, scale=(1.2, 1, 0.9))]
    for sx in (-1, 1):
        parts.append(sphere((loc[0] + sx * s * 0.3, loc[1], loc[2] + s * 1.55), s * 0.14, m))
        parts.append(sphere((loc[0] + sx * s * 0.45, loc[1] - s * 0.1, loc[2] + s * 0.6), s * 0.17, m, scale=(1, 1, 1.6)))
        parts.append(sphere((loc[0] + sx * s * 0.25, loc[1] - s * 0.2, loc[2] + s * 0.08), s * 0.18, m, scale=(1, 1.3, 0.8)))
        parts.append(sphere((loc[0] + sx * s * 0.13, loc[1] - s * 0.33, loc[2] + s * 1.33), s * 0.045, e))
    parts.append(sphere((loc[0], loc[1] - s * 0.44, loc[2] + s * 1.2), s * 0.05, e))
    return group("teddy", parts, loc)


def toy_robot(loc, s, shiny=True):
    m = mat("rob", (0.75, 0.78, 0.82), 0.15, metal=0.9 if shiny else 0.3); r = mat("robr", (0.85, 0.1, 0.1), 0.3, coat=0.5)
    eye = mat("robeye", (0.1, 0.8, 1.0), 0.2, emit=(0.2, 0.8, 1.0), emit_str=4)
    parts = [cube((loc[0], loc[1], loc[2] + s * 0.55), (s * 0.7, s * 0.5, s * 0.6), m, bevel=s * 0.05),
             cube((loc[0], loc[1], loc[2] + s * 1.1), (s * 0.5, s * 0.45, s * 0.4), m, bevel=s * 0.05),
             cyl((loc[0], loc[1], loc[2] + s * 1.4), s * 0.02, s * 0.2, r),
             sphere((loc[0], loc[1], loc[2] + s * 1.52), s * 0.05, r)]
    for sx in (-1, 1):
        parts.append(cube((loc[0] + sx * s * 0.15, loc[1], loc[2] + s * 0.12), (s * 0.18, s * 0.3, s * 0.26), r, bevel=s * 0.03))
        parts.append(cube((loc[0] + sx * s * 0.45, loc[1], loc[2] + s * 0.6), (s * 0.14, s * 0.2, s * 0.45), m, bevel=s * 0.03))
        parts.append(sphere((loc[0] + sx * s * 0.11, loc[1] - s * 0.23, loc[2] + s * 1.13), s * 0.06, eye))
    return group("robot", parts, loc)


def toy_dino(loc, s, col):
    m = mat("dino", col, 0.35, coat=0.3)
    parts = [sphere((loc[0], loc[1], loc[2] + s * 0.5), s * 0.45, m, scale=(1.5, 0.8, 0.9)),
             sphere((loc[0] + s * 0.65, loc[1], loc[2] + s * 1.0), s * 0.25, m, scale=(1.4, 0.8, 0.8)),
             sphere((loc[0] + s * 0.4, loc[1], loc[2] + s * 0.8), s * 0.17, m, scale=(1, 1, 1.8)),
             sphere((loc[0] - s * 0.75, loc[1], loc[2] + s * 0.4), s * 0.2, m, scale=(2.2, 0.6, 0.6))]
    for dx in (-0.25, 0.25):
        parts.append(cyl((loc[0] + dx * s, loc[1] - s * 0.1, loc[2] + s * 0.12), s * 0.1, s * 0.25, m))
    for dy in (-0.1, 0.1):
        parts.append(sphere((loc[0] + s * 0.82, loc[1] + dy * s, loc[2] + s * 1.07), s * 0.035, mat("eye", BLACK, 0.2)))
    return group("dino", parts, loc)


def toy_mouse(loc, s=0.1):
    m = mat("mouse", (0.55, 0.55, 0.6), 0.6, noise=0.2); pk = mat("pink", PINK, 0.8, sheen=0.6)
    x, y, z = loc
    parts = [sphere((x, y, z + s * 0.45), s * 0.5, m, scale=(1.5, 0.9, 0.8)), sphere((x + s * 0.7, y, z + s * 0.5), s * 0.28, m),
             sphere((x + s * 0.75, y - s * 0.18, z + s * 0.78), s * 0.15, pk), sphere((x + s * 0.75, y + s * 0.18, z + s * 0.78), s * 0.15, pk),
             sphere((x + s * 0.98, y, z + s * 0.48), s * 0.06, pk), cyl((x - s * 0.8, y, z + s * 0.3), s * 0.03, s * 0.8, m, rot=(0, 1.2, 0)),
             cyl((x, y + s * 0.5, z + s * 0.55), s * 0.12, s * 0.04, mat("key", (0.8, 0.6, 0.2), 0.3, metal=1), rot=(math.pi / 2, 0, 0))]
    for dy in (-0.1, 0.1): parts.append(sphere((x + s * 0.9, y + dy * s, z + s * 0.6), s * 0.04, mat("bead", BLACK, 0.15)))
    return group("mouse", parts, loc)


def dust(o, amt=0.5):
    """Grey dust layer over a toy (old, forgotten toys)."""
    for c in ([o] + list(o.children_recursive)):
        if c.type != "MESH": continue
        for i, m in enumerate(c.data.materials):
            if m is None: continue
            key = m.name + f"_dust{amt:.2f}"
            nm = bpy.data.materials.get(key)
            if nm is None:
                nm = m.copy(); nm.name = key; b = bsdf(nm)
                col = b.inputs["Base Color"].default_value
                b.inputs["Base Color"].default_value = tuple(col[k] * (1 - amt) + 0.35 * amt for k in range(3)) + (1,)
                b.inputs["Roughness"].default_value = 0.95; b.inputs["Coat Weight"].default_value = 0.0
            c.data.materials[i] = nm


def floor_toys(rng, spots):
    """spots: [(kind, loc, *args)] with kind in teddy/robot/dino/duck/ball/block/mouse."""
    out = []
    for kind, loc, *a in spots:
        if kind == "teddy": out.append(toy_teddy(loc, a[0], a[1], worn=a[2] if len(a) > 2 else 0.1))
        elif kind == "robot": out.append(toy_robot(loc, a[0]))
        elif kind == "dino": out.append(toy_dino(loc, a[0], a[1]))
        elif kind == "duck": out.append(toy_duck(loc, a[0]))
        elif kind == "ball": out.append(toy_ball(loc, a[0], rng))
        elif kind == "block": out.append(toy_block(loc, a[0], rng))
        elif kind == "mouse": out.append(toy_mouse(loc, a[0]))
    return out


# ---------------------------------------------------------------- Bun-Bun
BUNBUN_SCALE = 0.38                                  # about 50 cm tall in the toy room


def bunbun(loc, s=BUNBUN_SCALE, rot_z=0.0, worn=True, name="bunbun", ear_droop=0.6):
    fur = mat("fur", FUR if worn else (0.92, 0.86, 0.78), 0.95, sheen=1.0, noise=0.45 if worn else 0.1)
    fur_d = mat("furd", FUR_D, 0.95, sheen=1.0, noise=0.4); pink = mat("pink", PINK, 0.8, sheen=0.6)
    btn = mat("button", (0.02, 0.02, 0.025), 0.12, coat=1.0); thread = mat("thread", (0.55, 0.10, 0.10), 0.7)
    belly = mat("belly", (0.88, 0.80, 0.68), 0.95, sheen=1, noise=0.4)
    x, y, z = loc; P = []
    P.append(sphere((x, y, z + 0.30 * s), 0.30 * s, fur, scale=(1, 0.85, 1.05), name="body"))
    P.append(sphere((x, y - 0.17 * s, z + 0.30 * s), 0.18 * s, belly, scale=(1, 0.5, 1.2)))
    P.append(sphere((x, y - 0.02 * s, z + 0.78 * s), 0.25 * s, fur, scale=(1.05, 0.95, 0.95), name="head"))
    P.append(sphere((x, y - 0.22 * s, z + 0.72 * s), 0.10 * s, belly, scale=(1.3, 0.7, 0.9)))
    P.append(sphere((x, y - 0.29 * s, z + 0.76 * s), 0.035 * s, pink, scale=(1.3, 1, 0.9)))
    for sx in (-1, 1):                                                                   # button eyes
        ex, ey, ez = x + sx * 0.10 * s, y - 0.215 * s, z + 0.84 * s
        P.append(cyl((ex, ey, ez), 0.042 * s, 0.025 * s, btn, rot=(math.pi / 2, 0, 0), bevel=0.006 * s))
        for hx, hz in ((-0.012, 0.012), (0.012, 0.012), (-0.012, -0.012), (0.012, -0.012)):
            P.append(cyl((ex + hx * s, ey - 0.014 * s, ez + hz * s), 0.006 * s, 0.006 * s, mat("hole", (0.3, 0.3, 0.32), 0.5), rot=(math.pi / 2, 0, 0), verts=8))
    P.append(sphere((x - 0.10 * s, y, z + 1.17 * s), 0.07 * s, fur, scale=(0.9, 0.5, 3.4), rot=(0, -0.18, 0), name="earL"))
    P.append(sphere((x - 0.10 * s, y - 0.025 * s, z + 1.15 * s), 0.045 * s, pink, scale=(0.8, 0.3, 3.0), rot=(0, -0.18, 0)))
    P.append(sphere((x + 0.20 * s, y, z + 1.02 * s), 0.07 * s, fur_d, scale=(0.9, 0.5, 3.2), rot=(0, 0.25 + ear_droop, 0), name="earR"))
    for k in range(5):                                                                   # crooked stitches on the right ear
        a = -0.35 + k * 0.17
        P.append(cyl((x + 0.13 * s + a * 0.12 * s, y - 0.06 * s, z + 0.98 * s + math.sin(k) * 0.01 * s), 0.007 * s, 0.07 * s, thread, rot=(0, 0.9 + 0.2 * (k % 2), 0.3), verts=8))
    for sx in (-1, 1):
        P.append(sphere((x + sx * 0.27 * s, y - 0.06 * s, z + 0.35 * s), 0.09 * s, fur, scale=(1, 1, 1.9), rot=(0, sx * 0.45, 0)))
        P.append(sphere((x + sx * 0.14 * s, y - 0.18 * s, z + 0.06 * s), 0.10 * s, fur, scale=(1, 1.5, 0.7)))
        P.append(sphere((x + sx * 0.14 * s, y - 0.31 * s, z + 0.06 * s), 0.05 * s, pink, scale=(1, 0.3, 0.8)))
    P.append(sphere((x - 0.12 * s, y - 0.20 * s, z + 0.42 * s), 0.035 * s, mat("patch", (0.35, 0.45, 0.65), 0.9, sheen=0.8, noise=0.3), scale=(1.6, 0.4, 1.4)))
    g = group(name, P, loc); g.rotation_euler[2] = rot_z
    return g


# ---------------------------------------------------------------- the Lost Toy Room
def shelf(rng, loc, width, rows, dusty, rot=0.0):
    x, y, z = loc; wm = mat("shelfwood", WOOD, 0.6, noise=0.7)
    depth = 0.45; height = 3.6; gap = height / rows
    P = [cube((x, y + depth / 2 - 0.02, z + height / 2), (width, 0.04, height), mat("shelfback", WOOD_D, 0.8, noise=0.6))]
    for sx in (-1, 1): P.append(cube((x + sx * width / 2, y, z + height / 2), (0.06, depth, height), wm, bevel=0.01))
    for r in range(rows + 1): P.append(cube((x, y, z + r * gap + 0.02), (width, depth, 0.04), wm, bevel=0.01))
    toys = []
    for r in range(rows):
        zz = z + r * gap + 0.04; cx = x - width / 2 + 0.12
        while cx < x + width / 2 - 0.15:
            k = rng.random(); s = rng.uniform(0.22, 0.34); yy = y + rng.uniform(-0.08, 0.02)
            if k < 0.22: o = toy_block((cx + s / 2, yy, zz + s / 2), s * 0.9, rng); w = s
            elif k < 0.38: o = toy_ball((cx + s / 2, yy, zz), s * 0.5, rng); w = s
            elif k < 0.55: o = toy_car((cx + s * 0.9, yy, zz), s * 0.5, rng); w = s * 1.9
            elif k < 0.68: o = toy_duck((cx + s * 0.5, yy, zz), s * 0.8); w = s * 1.2
            elif k < 0.85: o = toy_teddy((cx + s * 0.5, yy, zz), s * 0.75, rng.choice([(0.55, 0.32, 0.15), (0.8, 0.6, 0.4), (0.7, 0.3, 0.35), (0.4, 0.4, 0.55)])); w = s * 1.1
            else: o = toy_dino((cx + s * 0.8, yy, zz), s * 0.5, rng.choice(TOYC)); w = s * 1.7
            if dusty and rng.random() < 0.7: dust(o, rng.uniform(0.2, 0.55))
            toys.append(o); cx += w + rng.uniform(0.0, 0.04)
    g = group("shelf", P, loc); g.rotation_euler[2] = rot
    for t in toys: t.parent = g; t.location = Vector(t.location) - Vector(loc)
    return g


def door(loc, open_amt=0.0, hall=False, hall_power=900):
    """Door with the LOST TOYS rule sign. open_amt 0..1.5 swings it open; hall=True lights a bright hallway beyond."""
    x, y, z = loc
    frame_m = mat("doorframe", WOOD_D, 0.6, noise=0.5); dm = mat("door", (0.28, 0.13, 0.06), 0.55, noise=0.7)
    cube((x - 0.62, y - 0.02, z + 1.15), (0.12, 0.22, 2.3), frame_m); cube((x + 0.62, y - 0.02, z + 1.15), (0.12, 0.22, 2.3), frame_m)
    cube((x, y - 0.02, z + 2.33), (1.36, 0.22, 0.12), frame_m)
    hinge = empty("hinge", (x - 0.56, y - 0.05, z)); bpy.context.view_layer.update()
    parts = [cube((x, y - 0.05, z + 1.13), (1.12, 0.07, 2.26), dm, bevel=0.01, name="doorpanel")]
    for zz in (0.5, 1.15): parts.append(cube((x, y - 0.09, z + zz), (0.8, 0.02, 0.5), mat("doorinset", (0.22, 0.10, 0.05), 0.6, noise=0.6), bevel=0.02))
    parts.append(sphere((x + 0.42, y - 0.12, z + 1.0), 0.045, mat("brass", (0.8, 0.55, 0.2), 0.25, metal=1.0)))
    sm = mat("sign", (0.86, 0.80, 0.64), 0.8, noise=0.25); ink = mat("signink", (0.06, 0.04, 0.03), 0.6)
    parts.append(cube((x, y - 0.095, z + 1.78), (0.74, 0.02, 0.56), sm, bevel=0.01))
    parts.append(text("LOST TOYS", (x, y - 0.108, z + 1.95), 0.13, ink))
    parts.append(text("A TOY MAY LEAVE\nONLY WHEN\nSOMEONE REMEMBERS IT", (x, y - 0.108, z + 1.70), 0.052, ink))
    for o in parts: o.parent = hinge; o.matrix_parent_inverse = hinge.matrix_world.inverted()
    hinge.rotation_euler[2] = open_amt * 1.6
    if hall:
        cube((x, y + 1.2, z + 1.5), (3, 0.05, 3), mat("hall", (1, 0.9, 0.7), 0.5, emit=(1.0, 0.82, 0.55), emit_str=9))
        cube((x, y + 0.6, z - 0.04), (3, 1.2, 0.1), mat("hallfloor", (0.6, 0.5, 0.4), 0.6))
        light("AREA", (x, y + 0.9, z + 1.3), hall_power, col=(1.0, 0.82, 0.58), size=1.0, rot=(-math.pi / 2, 0, 0))
    return hinge


def room(rng, shelf_rows=5, dusty=True, bulb=True, bulb_power=45, door_mode=False, door_open=0.0, hall=False, fill=60, hall_power=900):
    """The Lost Toy Room: wooden floor, toy shelves, one hanging bulb; door_mode puts the rule door at x=2.1 on the back wall."""
    floor_m = mat("floor", FLOOR, 0.55, noise=0.6); wall_m = mat("wall", WALL, 0.9, noise=0.35)
    cube((0, 0, -0.05), (14, 14, 0.1), floor_m, name="floor")
    for i in range(-14, 15): cube((i * 0.28, 0, 0.001), (0.006, 14, 0.002), mat("gap", (0.05, 0.025, 0.01), 0.9), name="gap")
    if door_mode:
        cube((-2.6, 3.2, 2.5), (8.8, 0.1, 5), wall_m); cube((5.33, 3.2, 2.5), (5.34, 0.1, 5), wall_m); cube((2.1, 3.2, 3.63), (1.12, 0.1, 2.74), wall_m)
    else:
        cube((0, 3.2, 2.5), (14, 0.1, 5), wall_m, name="backwall")
    cube((-4.2, 0, 2.5), (0.1, 14, 5), wall_m); cube((4.2, 0, 2.5), (0.1, 14, 5), wall_m)
    for x0 in ((-2.05, 0.0) if door_mode else (-2.05, 0.0, 2.05)): shelf(rng, (x0, 2.75, 0), 1.9, shelf_rows, dusty)
    shelf(rng, (-3.7, 0.9, 0), 1.7, shelf_rows, dusty, rot=math.pi / 2)
    if door_mode: door((2.1, 3.2, 0), door_open, hall, hall_power)
    if bulb:
        cyl((0.2, 0.9, 4.3), 0.008, 1.4, mat("cord", (0.02, 0.02, 0.02), 0.6))
        cyl((0.2, 0.9, 3.55), 0.05, 0.1, mat("sock", (0.15, 0.12, 0.08), 0.4, metal=0.8))
        sphere((0.2, 0.9, 3.42), 0.09, mat("bulb", (1, 0.85, 0.6), 0.1, emit=(1.0, 0.65, 0.3), emit_str=40), name="bulb")
        light("POINT", (0.2, 0.9, 3.30), bulb_power * 10, col=(1.0, 0.62, 0.32), size=0.1)
    if fill: light("AREA", (2.5, -3.5, 3.5), fill, col=(0.35, 0.42, 1.0), size=4, target=(0, 1.5, 1))


def figure(loc, h, hunch=0.0, name="fig"):
    """A soft dark human silhouette (grown-ups seen from a toy's point of view)."""
    m = mat("silhouette", (0.012, 0.01, 0.012), 0.9); x, y, z = loc; P = []
    P.append(sphere((x, y, z + h * 0.55), h * 0.17, m, scale=(1.05, 0.75, 2.2)))
    P.append(sphere((x, y + hunch * h * 0.12, z + h * 0.9), h * 0.085, m))
    for sx in (-1, 1):
        P.append(sphere((x + sx * h * 0.06, y, z + h * 0.2), h * 0.05, m, scale=(1, 1, 4.5)))
        P.append(sphere((x + sx * h * 0.19, y + hunch * h * 0.05, z + h * 0.55), h * 0.04, m, scale=(1, 1, 5.5), rot=(0, sx * 0.15, 0)))
    g = group(name, P, loc); g.rotation_euler[0] = hunch * 0.25
    return g


def sparkles(center, n, radius, rng, strength=30, size=0.012):
    m = mat("spark", (1, 0.9, 0.6), 0.2, emit=(1.0, 0.85, 0.5), emit_str=strength)
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi); r = radius * math.sqrt(rng.random()); h = rng.uniform(-radius, radius)
        sphere((center[0] + math.cos(a) * r, center[1] + math.sin(a) * r * 0.5, center[2] + h), size * rng.uniform(0.5, 1.4), m, seg=8)


def dust_motes(rng, n=160, box=((-3, 3), (-2, 2.5), (0.3, 3.8))):
    m = mat("mote", (1, 0.9, 0.7), 0.5, emit=(1.0, 0.8, 0.55), emit_str=1.5)
    for _ in range(n):
        sphere((rng.uniform(*box[0]), rng.uniform(*box[1]), rng.uniform(*box[2])), rng.uniform(0.0015, 0.0035), m, seg=6)
