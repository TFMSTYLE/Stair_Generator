# Stair Generator

![stair-thumb](https://github.com/user-attachments/assets/5d8f6943-a175-486e-9cc5-ba828dae7189)

**Author:** The French Monkey (TFMSTYLE)  
**Version:** 1.0.0  

---

## Overview

The Stair Generator is a procedural tool for creating **parametric staircases** directly inside Blender.  
It supports three staircase types — **Straight**, **Spiral**, and **L-Shaped** — each generated mathematically from user-defined parameters.  
Designed for architectural visualization, modeling workflows, and parametric design, the add-on allows fast iteration and real-time updates through its **Live Update** system.

---

## Parameters

### Live Update
When enabled, automatically rebuilds the staircase every time a parameter is changed.  
Disabling this option allows for manual updates using the **Generate Stairs** operator.

---

### Type
Selects the staircase configuration to generate.  

Available types:  
- **Straight:** Linear flight with uniform rise and run.  
- **Spiral:** Cylindrical staircase revolving around a central axis.  
- **L-Shaped:** Two flights joined at a 90° corner with a platform.

---

### Steps
Defines the number of stair steps.  
Each step’s height and depth are derived from this value to maintain proportional scaling.

---

### Width
Sets the total width of each step measured perpendicular to the stair direction.

---

### Depth
Specifies the run length of each step (the horizontal distance from front to back).

---

### Height
Determines the rise per step (the vertical increment between steps).

---

### Thickness
Defines the geometric thickness of each step, controlling the solid extrusion depth.

---

### Inner Radius
Used exclusively for **Spiral** stairs.  
Defines the distance from the central axis to the inner edge of the steps.

---

### Rotation
Used exclusively for **Spiral** stairs.  
Determines the total angular rotation in degrees from the first to the last step.

---

### Turn at Step
Used exclusively for **L-Shaped** stairs.  
Specifies at which step the staircase makes its 90° turn and introduces the landing platform.

---

## Operators

### Generate Stairs
Creates a new staircase mesh based on the selected type and parameters.  
If a previously generated stair object is selected, it will update in place instead of creating a new one.  
Applies all current values from the **Stair Generator** panel and rebuilds the mesh geometry accordingly.

---

## Usage Notes

- For **architectural modeling**, match **Step Height** and **Step Depth** to real-world standards.  
- When using **Live Update**, parameter changes instantly update the model in the viewport.  
- **Spiral stairs** use **Inner Radius** and **Rotation** to define curvature and revolution.  
- **L-Shaped stairs** generate a landing platform at the specified **Turn at Step** position.  
- Generated stairs are non-destructive and can be modified parametrically until converted to a mesh.  
- Works seamlessly with Blender’s geometry nodes or array modifiers for extended procedural control.
