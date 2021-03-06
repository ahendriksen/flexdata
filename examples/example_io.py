#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test reading Flexray raw and writing ASTRA readable
"""
#%%

from flexdata import io

#%% Read / write a geometry file:

path = '/ufs/ciacc/flexbox/al_test/90KV_no_filt/'

meta = io.read_meta(path, 'flexray')

io.write_toml(path + 'flexray.toml', meta)

#%% Read / write raw data files:
    
dark = io.read_tiffs(path, 'di00')
flat = io.read_tiffs(path, 'io00')    
proj = io.read_tiffs(path, 'scan_')

#%% Read geometry and convert to ASTRA:

meta_1 = io.read_toml(path + 'flexray.toml') 

vol_geom =  io.astra_vol_geom(meta['geometry'], [100, 100, 100])
proj_geom =  io.astra_proj_geom(meta['geometry'], proj.shape)
    
print(vol_geom)
print(proj_geom)
