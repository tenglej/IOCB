# ————————————————————————————
# Load & initial styling
# ————————————————————————————
# from pymol import cmd, stored


hide everything
bg_color white

show cartoon
set cartoon_transparency, 0.6
color salmon

# ————————————————————————————
# Substrate sticks & coloring
# ————————————————————————————
create subselection, sele
show sticks, sub*
set stick_radius, 0.2, sub*
color white,  sub* and elem C
color white,  sub* and elem H
color red,    sub* and elem O
color blue,   sub* and elem N
color orange, sub* and elem S

# ————————————————————————————
# Surrounding residue sidechains
# ————————————————————————————
select near_residues,     byres(br. sub* around 5) and polymer.protein and not sub*
select near_sidechains,   near_residues and not name N+CA+C+O

show sticks, near_sidechains
set stick_radius, 0.2, near_sidechains
color white,  near_sidechains and elem C
color white,  near_sidechains and elem H
color red,    near_sidechains and elem O
color blue,   near_sidechains and elem N
color orange, near_sidechains and elem S

# hide all sidechain H’s by default
hide sticks, near_sidechains and elem H

# ————————————————————————————
# Water (solvent) near substrate shown as sticks
# ————————————————————————————
select water_near_substrate, solvent within 4 of sub*
show sticks, water_near_substrate
set stick_radius, 0.2, water_near_substrate
color white, water_near_substrate and elem H
color red,   water_near_substrate and elem O


# ————————————————————————————
# Copper & Dioxygen
# ————————————————————————————
select copper_atoms, elem Cu
select Iron_atoms, elem Fe
select metals, copper_atoms or Iron_atoms or elem Zn or elem Ni
show spheres, metals
color orange, copper_atoms
color orange, metals 
set sphere_scale, 0.35, metals

select nearby_oxygens, elem O within 2.5 of metals
show spheres, nearby_oxygens
color red, nearby_oxygens
set sphere_scale, 0.25, nearby_oxygens


# ————————————————————————————
# Combined H‑bond definitions (sub*, Cu, O2, waters)
# ————————————————————————————

# 1. H’s on sidechains near sub*
select hb_H_sub_sc, (near_sidechains and elem H) within 3.5 of sub*
# 2. H’s on waters near sub*
select hb_H_sub_w,  (water_near_substrate and elem H)  within 3.5 of sub*
# 3. Show those H’s
show sticks, hb_H_sub_sc hb_H_sub_w

# 4. Draw H‑bonds to sub* (N/O acceptors)
distance hb_substrate_sidechain, (sub* and elem N+O), hb_H_sub_sc, 3.5
distance hb_substrate_water,  (sub* and elem N+O), hb_H_sub_w,  3.5

# 5. H’s on sidechains near Cu/O2
select sidechains_near_centre, (near_sidechains and elem H) within 3.5 of(water_near_substrate or nearby_oxygens)
# 6. H’s on waters near Cu/O2
select water_near_centre,  (water_near_metal and elem H) within 3.5 of(water_near_substrate or nearby_oxygens)
# 7. Show those H’s
show sticks, sidechains_near_centre water_near_centre

# 8. Draw H‑bonds to Cu/O2
distance hb_metal_sidechain, (water_near_substrate or nearby_oxygens), sidechains_near_centre, 3.5
distance hb_metal_water,  (water_near_substrate or nearby_oxygens), water_near_centre,  3.5

# 9. Style all H‑bonds as yellow dashed lines
set dash_color,   yellow, hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water
set dash_width,   2,      hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water
set dash_gap,     0.3,    hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water
set dash_length,  0.2,    hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water

# 10. Hide all numeric labels
hide labels, hb_substrate_sidechain hb_subhb_metal_sidechain hb_metal_water


# ————————————————————————————
# Waters near Cu/O2 shown as sticks
# ————————————————————————————
select water_near_metal, solvent within 4 of(metals or nearby_oxygens)
show sticks, water_near_metal
set stick_radius, 0.2, water_near_metal
color white, water_near_metal and elem H
color red,   water_near_metal and elem O

# ————————————————————————————
# Hydrogen‑bond dashed lines & showing H’s
# ————————————————————————————


# 1. H‑bonds to the substrate (sidechain + water H’s)
select hb_H_sub_sc, (near_sidechains and elem H) within 3.5 of sub*
select hb_H_sub_w,  (water_near_substrate and elem H)  within 3.5 of sub*
# show those H’s as sticks
show sticks, hb_H_sub_sc hb_H_sub_w

distance hb_substrate_sidechain, (sub* and elem N+O), hb_H_sub_sc, 3.5
distance hb_substrate_water,  (sub* and elem N+O), hb_H_sub_w,  3.5

# 2. H‑bonds to Cu/O2 via sidechain H’s
select sidechains_near_centre, (near_sidechains and elem H) within 3.5 of(water_near_substrate or nearby_oxygens)
show sticks, sidechains_near_centre
distance hb_metal_sidechain, (water_near_substrate or nearby_oxygens), sidechains_near_centre, 3.5

# 3. H‑bonds to Cu/O2 via water H’s
select water_near_centre,  (water_near_substrate or water_near_metal and elem H) within 3.5 of(water_near_substrate or nearby_oxygens)
show sticks, water_near_centre
distance hb_metal_water,  (water_near_substrate or nearby_oxygens), water_near_centre, 3.5

# 4. Style all H‑bonds as yellow dashed lines
set dash_color,   yellow, hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water
set dash_width,   2,      hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water
set dash_gap,     0.3,    hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water
set dash_length,  0.2,    hb_substrate_sidechain hb_substrate_water hb_metal_sidechain hb_metal_water

# 5. Hide the numeric labels
select hydrogen_bonds, hb_substrate_sidechain or hb_substrate_water or hb_metal_sidechain or hb_metal_water
hide labels, hydrogen_bonds

# ———————————————————————————————————
# Copper & Dioxygen + bonding
# ———————————————————————————————————

# Show direct bonds from Cu to nearby heavy atoms only
select metal_coordination, (not elem H and not metals) within 2.25 of metals

# --- START PYTHON BLOCK ---
python
from pymol import cmd
from math import sqrt

MAX_DISTANCE = 2.3  # Å

def get_distance(atom1, atom2):
    dx = atom1.coord[0] - atom2.coord[0]
    dy = atom1.coord[1] - atom2.coord[1]
    dz = atom1.coord[2] - atom2.coord[2]
    return sqrt(dx*dx + dy*dy + dz*dz)

copper_atoms = cmd.get_model("copper_atoms").atom
nearby_atoms = cmd.get_model("metal_coordination").atom

for cu_atom in copper_atoms:
    for other_atom in nearby_atoms:
        if cu_atom.index == other_atom.index:
            continue
        dist = get_distance(cu_atom, other_atom)
        if dist <= MAX_DISTANCE:
            cmd.bond(f"index {cu_atom.index}", f"index {other_atom.index}")
python end

# --- END PYTHON BLOCK ---


# Example PML commands after the Python block
show sticks, metals or metal_coordination
set stick_radius, 0.1, metals or metal_coordination
zoom metals or metal_coordination

