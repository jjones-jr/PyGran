'''
Created on April 22, 2017
@author: Andrew Abi-Mansour
'''

# !/usr/bin/python
# -*- coding: utf8 -*-

from PyGran import Simulator, Visualizer
from PyGran.Materials import glass, stearicAcid
import os

glass['youngsModulus'] = 1e9

pDict = {
		# Define the system
		'boundary': ('f','f','f'),
		'box':  (-1e-3, 1e-3, -1e-3, 1e-3, 0, 4e-3),

		# Define component(s)
		'SS': ({'material': stearicAcid, 'radius': ('constant', 5e-5)},),

		# Setup I/O params
		'traj': {'freq':1000, 'style': 'custom/vtk', 'pfile': 'traj*.vtk', 'mfile': 'mesh*.vtk'},
		'output': 'test',

		# Define computational parameters
		'dt': 1e-6,

		# Apply a gravitional force in the negative direction along the z-axis
		'gravity': (9.81, 0, 0, -1),

		# Import hopper mesh
		 'mesh': {
			'hopper': {'file': 'silo.stl', 'mtype': 'mesh/surface', 'import': True, 'material': glass, 'args': ('scale 1e-3',)},
			'valve': {'file': 'valve.stl', 'mtype': 'mesh/surface', 'import': True, 'material': glass, 'args': ('move 0 0 1.0', 'scale 1e-3',)},
		      },

		# Stage runs
		'stages': {'insertion': 1e4, 'run': 1e4},
	  }

# Create an instance of the DEM class
sim = Simulator.DEM(**pDict)

# Setup a stopper wall along the xoy plane
stopper = sim.setupWall(species=1, wtype='primitive', plane = 'zplane', peq = 0.0)

sim.moveMesh('valve', 'rotate origin 0. 0. 0.', 'axis  0. 0. 1.', 'period 5e-2')

# Insert particles in a cubic region
insert = sim.insert(species=1, region=('block', -5e-4, 5e-4, -5e-4, 5e-4, 2e-3, 3e-3), value=100)
sim.run(pDict['stages']['insertion'], pDict['dt'])
sim.remove(insert)

# Run equilibration run
sim.run(pDict['stages']['run'], pDict['dt'])

# Remove stopper and monitor flow
sim.remove(stopper)
sim.run(pDict['stages']['run'], pDict['dt'])