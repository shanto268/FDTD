import fdtd as f

#A grid is defined by its shape, which is just a 3D tuple of Number-types (integers or floats). If the shape is given in floats, it denotes the width, height and length of the grid in meters. If the shape is given in integers, it denotes the width, height and length of the grid in terms of the grid_spacing

grid = f.Grid(shape = (25e-6, 15e-6, 1), 
    grid_spacing= 155e-9,
    permittivity = 1.0,
    permeability = 1.0, 
    courant_number = 0.70)

grid[11:32, 30:84, 0] = f.Object(permittivity=1.7**2, name="object1")

grid[13e-6:18e-6, 5e-6:8e-6, 0] = f.Object(permittivity=1.5**2, name="object2")

"""
f.LineSource(
    period: Number = 15, # timesteps or seconds
    power: float = 1.0,
    phase_shift: float = 0.0,
    name: str = None,
)
"""

grid[7.5e-6:8.0e-6, 11.8e-6:13.0e-6, 0] = f.LineSource(
    period = 1550e-9 / (3e8), name="source2"
)

"""
grid[12e-6:22.0e-6, 1.8e-6:1.9E-6, 0] = f.LineSource(
    period = 5, name="source1", power = 3.0
)
"""

grid[12e-6, :, 0] = f.LineDetector(name="detector")


"""
#Defining boundaries
fdtd.PML(
    a: float = 1e-8, # stability factor
    name: str = None
)
"""

# x boundaries
grid[0:10, :, :] = f.PML(name="pml_xlow")
grid[-10:, :, :] = f.PML(name="pml_xhigh")

# y boundaries
grid[:, 0:10, :] = f.PML(name="pml_ylow")
grid[:, -10:, :] = f.PML(name="pml_yhigh")


#print(grid.detector)
#print(grid.source)
#print(grid.objects)
print(grid)

#running sim
grid.run(
    total_time = int(input("For how many seconds to you want the simulation to last? ")), #seconds
    progress_bar = False
)

#visualize
"""
grid.visualize(
    grid,
    x=None,
    y=None,
    z=None,
    cmap="Blues",
    pbcolor="C3",
    pmlcolor=(0, 0, 0, 0.1),
    objcolor=(1, 0, 0, 0.1),
    srccolor="C0",
    detcolor="C2",
    show=True
)
"""

grid.visualize(z=0)
