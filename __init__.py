# SPDX-FileCopyrightText: 2025-2026 The French Monkey
# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Stair",
    "author": "The French Monkey",
    "version": (1, 0, 1),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Stair",
    "description": "Generate parametric stairs",
    "category": "Add Mesh",
    "license": "GPL-3.0-or-later",
}

import bpy
import bmesh
from math import radians, sin, cos

# ------------------------------------------------------------------------
# Stair Geometry Generators
# ------------------------------------------------------------------------

def create_straight_stairs(steps, step_width, step_depth, step_height, thickness):
    verts, faces, v_idx = [], [], 0
    for i in range(steps):
        z, y = i * step_height, i * step_depth
        step_verts = [
            (-step_width/2, y, z), (step_width/2, y, z),
            (step_width/2, y + step_depth, z), (-step_width/2, y + step_depth, z),
            (-step_width/2, y, z + thickness), (step_width/2, y, z + thickness),
            (step_width/2, y + step_depth, z + thickness), (-step_width/2, y + step_depth, z + thickness)
        ]
        verts.extend(step_verts)
        base = v_idx
        step_faces = [
            (base+0, base+1, base+2, base+3), (base+4, base+7, base+6, base+5),
            (base+0, base+4, base+5, base+1), (base+2, base+6, base+7, base+3),
            (base+0, base+3, base+7, base+4), (base+1, base+5, base+6, base+2)
        ]
        faces.extend(step_faces)
        v_idx += 8
    return verts, faces

def create_spiral_stairs(steps, step_width, inner_radius, step_height, thickness, rotation, step_depth):
    verts, faces, v_idx = [], [], 0
    angle_per_step = radians(rotation / steps)
    outer_radius = inner_radius + step_width
    avg_radius = (inner_radius + outer_radius) / 2
    angular_depth = step_depth / avg_radius
    for i in range(steps):
        angle_start, angle_end, z = i * angle_per_step, i * angle_per_step + angular_depth, i * step_height
        cos_a1, sin_a1, cos_a2, sin_a2 = cos(angle_start), sin(angle_start), cos(angle_end), sin(angle_end)
        step_verts = [
            (inner_radius * cos_a1, inner_radius * sin_a1, z), (outer_radius * cos_a1, outer_radius * sin_a1, z),
            (outer_radius * cos_a2, outer_radius * sin_a2, z), (inner_radius * cos_a2, inner_radius * sin_a2, z),
            (inner_radius * cos_a1, inner_radius * sin_a1, z + thickness), (outer_radius * cos_a1, outer_radius * sin_a1, z + thickness),
            (outer_radius * cos_a2, outer_radius * sin_a2, z + thickness), (inner_radius * cos_a2, inner_radius * sin_a2, z + thickness)
        ]
        verts.extend(step_verts)
        base = v_idx
        step_faces = [
            (base+0, base+1, base+2, base+3), (base+4, base+7, base+6, base+5),
            (base+0, base+4, base+5, base+1), (base+2, base+6, base+7, base+3),
            (base+0, base+3, base+7, base+4), (base+1, base+5, base+6, base+2)
        ]
        faces.extend(step_faces)
        v_idx += 8
    return verts, faces

def create_l_shaped_stairs(steps, step_width, step_depth, step_height, thickness, turn_at_step):
    verts, faces, v_idx = [], [], 0
    platform_size = max(step_width, step_depth * 1.5)
    for i in range(steps):
        z = i * step_height
        if i < turn_at_step:
            y, x = i * step_depth, 0
            step_verts = [
                (x - step_width/2, y, z), (x + step_width/2, y, z),
                (x + step_width/2, y + step_depth, z), (x - step_width/2, y + step_depth, z),
                (x - step_width/2, y, z + thickness), (x + step_width/2, y, z + thickness),
                (x + step_width/2, y + step_depth, z + thickness), (x - step_width/2, y + step_depth, z + thickness)
            ]
        elif i == turn_at_step:
            y_base = turn_at_step * step_depth
            step_verts = [
                (-platform_size/2, y_base, z), (platform_size/2, y_base, z),
                (platform_size/2, y_base + platform_size, z), (-platform_size/2, y_base + platform_size, z),
                (-platform_size/2, y_base, z + thickness), (platform_size/2, y_base, z + thickness),
                (platform_size/2, y_base + platform_size, z + thickness), (-platform_size/2, y_base + platform_size, z + thickness)
            ]
        else:
            y_base = turn_at_step * step_depth + platform_size / 2
            x_offset = (i - turn_at_step - 1) * step_depth + platform_size / 2
            step_verts = [
                (x_offset, y_base - step_width/2, z), (x_offset + step_depth, y_base - step_width/2, z),
                (x_offset + step_depth, y_base + step_width/2, z), (x_offset, y_base + step_width/2, z),
                (x_offset, y_base - step_width/2, z + thickness), (x_offset + step_depth, y_base - step_width/2, z + thickness),
                (x_offset + step_depth, y_base + step_width/2, z + thickness), (x_offset, y_base + step_width/2, z + thickness)
            ]
        verts.extend(step_verts)
        base = v_idx
        faces.extend([
            (base+0, base+1, base+2, base+3), (base+4, base+7, base+6, base+5),
            (base+0, base+4, base+5, base+1), (base+2, base+6, base+7, base+3),
            (base+0, base+3, base+7, base+4), (base+1, base+5, base+6, base+2)
        ])
        v_idx += 8
    return verts, faces

def build_stair_mesh(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    return mesh

# ------------------------------------------------------------------------
# Rebuild / Generate
# ------------------------------------------------------------------------

def rebuild_stairs(obj):
    if not obj or obj.type != "MESH": return False
    stair_type, steps = obj["stair_type"], obj["steps"]
    step_width, step_depth, step_height, thickness = obj["step_width"], obj["step_depth"], obj["step_height"], obj["thickness"]
    if stair_type == "STRAIGHT":
        verts, faces = create_straight_stairs(steps, step_width, step_depth, step_height, thickness)
    elif stair_type == "SPIRAL":
        inner_radius, rotation = obj["inner_radius"], obj["rotation"]
        verts, faces = create_spiral_stairs(steps, step_width, inner_radius, step_height, thickness, rotation, step_depth)
    else:
        turn_at_step = obj["turn_at_step"]
        verts, faces = create_l_shaped_stairs(steps, step_width, step_depth, step_height, thickness, turn_at_step)
    mesh = build_stair_mesh("StairMesh", verts, faces)
    old = obj.data
    obj.data = mesh
    if old and old.users == 0: bpy.data.meshes.remove(old)
    return True

def generate_stairs(context):
    p, obj = context.scene.sgen_props, context.active_object
    keys = ("stair_type", "steps", "step_width", "step_depth", "step_height", "thickness", "inner_radius", "rotation", "turn_at_step")
    if obj and obj.type == "MESH" and "stair_generator" in obj and obj.select_get():
        for k in keys: obj[k] = getattr(p, k)
        rebuild_stairs(obj)
        obj.name = obj.data.name = f"Stairs_{p.stair_type}"
        return obj
    mesh = bpy.data.meshes.new("StairMesh")
    new_obj = bpy.data.objects.new(f"Stairs_{p.stair_type}", mesh)
    context.collection.objects.link(new_obj)
    context.view_layer.objects.active = new_obj
    new_obj.select_set(True)
    for k in keys: new_obj[k] = getattr(p, k)
    new_obj["stair_generator"] = True
    rebuild_stairs(new_obj)
    return new_obj

# ------------------------------------------------------------------------
# Live Update
# ------------------------------------------------------------------------

def update_stairs(self, context):
    p = context.scene.sgen_props
    if not p.live_update:
        return
    
    o = context.active_object
    if not (o and o.type == "MESH" and "stair_generator" in o and o.select_get()):
        return
    
    keys = ("stair_type", "steps", "step_width", "step_depth", "step_height",
            "thickness", "inner_radius", "rotation", "turn_at_step")
    for k in keys:
        o[k] = getattr(p, k)
    
    rebuild_stairs(o)

    new_name = f"Stairs_{p.stair_type}"
    if o.name != new_name:
        o.name = o.data.name = new_name

# ------------------------------------------------------------------------
# UI Properties
# ------------------------------------------------------------------------

class SGProperties(bpy.types.PropertyGroup):
    live_update: bpy.props.BoolProperty(
        name="Live Update",
        default=False,
        description="Update stairs in real-time as parameters change"
    )
    
    stair_type: bpy.props.EnumProperty(name="Type", items=[("STRAIGHT", "Straight", "Straight staircase"), ("SPIRAL", "Spiral", "Spiral staircase"), ("L_SHAPED", "L-Shaped", "L-shaped staircase with 90° turn")], default="STRAIGHT", update=update_stairs)
    steps: bpy.props.IntProperty(name="Steps", default=10, min=1, max=100, description="Number of steps", update=update_stairs)
    step_width: bpy.props.FloatProperty(name="Width", default=2.0, min=0.1, max=20.0, description="Width of each step", unit='LENGTH', update=update_stairs)
    step_depth: bpy.props.FloatProperty(name="Depth", default=0.3, min=0.1, max=5.0, description="Depth of each step", unit='LENGTH', update=update_stairs)
    step_height: bpy.props.FloatProperty(name="Height", default=0.2, min=0.01, max=2.0, description="Height of each step", unit='LENGTH', update=update_stairs)
    thickness: bpy.props.FloatProperty(name="Thickness", default=0.05, min=0.01, max=1.0, description="Thickness of each step", unit='LENGTH', update=update_stairs)
    inner_radius: bpy.props.FloatProperty(name="Inner Radius", default=1.0, min=0.1, max=10.0, description="Inner radius for spiral stairs", unit='LENGTH', update=update_stairs)
    rotation: bpy.props.FloatProperty(name="Rotation", default=360.0, min=45.0, max=1080.0, description="Total rotation in degrees", update=update_stairs)
    turn_at_step: bpy.props.IntProperty(name="Turn at Step", default=5, min=1, max=50, description="Step number where the stairs turn 90°", update=update_stairs)

# ------------------------------------------------------------------------
# Operators
# ------------------------------------------------------------------------

class SG_OT_generate(bpy.types.Operator):
    bl_idname = "sg.generate"
    bl_label = "Generate Stairs"
    bl_description = "Generate parametric stairs"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        generate_stairs(context)
        return {"FINISHED"}

# ------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------

class VIEW3D_PT_stair_generator(bpy.types.Panel):
    bl_label = "Stair"
    bl_idname = "VIEW3D_PT_stair_generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Stair"

    def draw(self, context):
        layout = self.layout
        p = context.scene.sgen_props
        o = context.object

        layout.operator("sg.generate", text="Generate Stairs", icon="MOD_ARRAY")

        layout.prop(p, "live_update", toggle=True)

        layout.separator(factor=0.5)

        layout.prop(p, "stair_type", expand=True)

        col = layout.column(align=True)
        col.prop(p, "steps", slider=True)
        col.prop(p, "step_width", slider=True)
        col.prop(p, "step_depth", slider=True)
        col.prop(p, "step_height", slider=True)
        col.prop(p, "thickness", slider=True)

        if p.stair_type == "SPIRAL":
            col.separator(factor=0.5)
            col.prop(p, "inner_radius", slider=True)
            col.prop(p, "rotation", slider=True)

        elif p.stair_type == "L_SHAPED":
            col.separator(factor=0.5)
            col.prop(p, "turn_at_step", slider=True)

        layout.separator(factor=0.5)

        if (
            o and o.type == "MESH"
            and "stair_generator" in o
            and o.select_get()
        ):
            layout.label(text=f"Editing Stair: {o.name}", icon="MOD_ARRAY")
        else:
            layout.label(text="No stair object selected", icon="INFO")

# ------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------

classes = (
    SGProperties,
    SG_OT_generate,
    VIEW3D_PT_stair_generator, 
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.sgen_props = bpy.props.PointerProperty(type=SGProperties)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.sgen_props

if __name__ == "__main__":
    register()