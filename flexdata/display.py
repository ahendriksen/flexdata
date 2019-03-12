#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: A. Kostenko
Created on Oct 2018

This module contains a few simple routines for displaying data.
"""

""" * Imports * """

import numpy

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import ticker

import pyqtgraph as pq

from . import array

""" * Methods * """
def plot3d(x, y, z, connected = False, title = None):
    '''
    Plot a 3D line or a scatter plot.
    '''
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z)
    
    if connected:
        ax.plot(x, y, z)
        
    _after_plot_(title, None)
    
def plot2d(x, y=None, semilogy=False, title=None, legend=None):

    if y is None:
        y = x
        x = numpy.arange(numpy.size(x))

    x = numpy.squeeze(x)
    y = numpy.squeeze(y)

    plt.figure()
    if semilogy:
        plt.semilogy(x, y)
    else:
        plt.plot(x, y)

    if title:
        plt.title(title)

    if legend:
        plt.legend(legend)

    plt.show()

def pyqt_graph(data, dim = 0, title=None):
    '''
    Create a PYQT window to display a 3D dataset.
    '''
    # create pyqtgraph app:
    app = pq.mkQApp()
    
    pq.image(numpy.rot90(numpy.rollaxis(data, dim), axes = (1,2)), title = title)

    app.exec_()

def slice(data, index=None, dim=0, bounds=None, title=None, cmap="gray", file=None):

    # Just in case squeeze:
    data = numpy.squeeze(data)

    # If the image is 2D:
    if data.ndim == 2:
        img = data

    else:
        if index is None:
            index = data.shape[dim] // 2

        sl = array.anyslice(data, index, dim)

        img = numpy.squeeze(data[sl])

        # There is a bug in plt. It doesn't like float16
        if img.dtype == "float16":
            img = numpy.float32(img)

    fig = plt.figure()

    if bounds:
        imsh = plt.imshow(img[::-1, :], vmin=bounds[0], vmax=bounds[1], cmap=cmap)
    else:
        imsh = plt.imshow(img[::-1, :], cmap=cmap)

    # plt.colorbar()
    cbar = fig.colorbar(imsh, ticks=ticker.MaxNLocator(nbins=6))
    cbar.ax.tick_params(labelsize=15)

    _after_plot_(title, file)
    
def _after_plot_(title, file):
    
    #plt.axis("off")

    if title:
        plt.title(title)

    plt.show()

    if file:
        plt.savefig(file, dpi=300, bbox_inches="tight")

def mesh(stl_mesh):
    """
    Display an stl mesh. Use flexCompute.generate_stl(volume) to generate mesh.
    """
    from mpl_toolkits import mplot3d

    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)

    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors))

    # Auto scale to the mesh size
    scale = stl_mesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    # Show the plot to the screen
    plt.show()


def projection(data, dim=1, bounds=None, title=None, cmap="gray", file=None):

    img = data.sum(dim)

    # There is a bug in plt. It doesn't like float16
    img = numpy.float32(img)

    plt.figure()

    if bounds:
        plt.imshow(img[::-1, :], vmin=bounds[0], vmax=bounds[1], cmap=cmap)
    else:
        plt.imshow(img[::-1, :], cmap=cmap)

    plt.colorbar()
    
    _after_plot_(title, file)


def color_project(data, dim=1, sample = 2, bounds=[0.01, 0.1], title=None, cmap='nipy_spectral', file=None):

    # Sample data:
    data = data[::sample,::sample,::sample]
    
    # Initialize colormap:
    cmap_ = plt.get_cmap(cmap)
    
    # Shape of the final image:
    shape = list(data.shape)
    shape.remove(shape[dim])
    shape.append(3)

    # Output image:    
    rgb_total = numpy.zeros(shape, dtype = 'float32')
    
    print('Applying colormap...')
    
    for ii in range(data.shape[dim]):
        
        sl = array.anyslice(data, ii, dim)
        img = numpy.squeeze(data[sl].copy())
        
        img[img > bounds[1]] = bounds[1]
        img[img < bounds[0]] = bounds[0]
        img -= bounds[0]
        img /= bounds[1] - bounds[0]
        
        rgba_img = cmap_(img)
        rgb_img = numpy.delete(rgba_img, 3, 2)
        
        rgb_total += rgb_img# / data.shape[dim]
        #rgb_total = numpy.max([rgb_img, rgb_total], axis = 0)
        
    #rgb_total /= rgb_total.max()
    #rgb_total = numpy.log(rgb_total)
    rgb_total = numpy.sqrt(rgb_total)
    
    plt.figure()
    
    plt.imshow(rgb_total[::-1, :] / rgb_total.max(), cmap = cmap)
    
    plt.colorbar()
    
    _after_plot_(title, file)

def max_projection(data, dim=0, bounds=None, title=None, cmap="gray", file=None):

    img = data.max(dim)

    # There is a bug in plt. It doesn't like float16
    img = numpy.float32(img)

    plt.figure()

    if bounds:
        plt.imshow(img[::-1, :], vmin=bounds[0], vmax=bounds[1], cmap=cmap)
    else:
        plt.imshow(img[::-1, :], cmap=cmap)

    plt.colorbar()
    _after_plot_(title, file)


def min_projection(data, dim=0, title=None, cmap="gray", file=None):

    img = data.min(dim)

    # There is a bug in plt. It doesn't like float16
    img = numpy.float32(img)

    plt.figure()

    plt.imshow(img[::-1, :], cmap=cmap)
    plt.colorbar()
    _after_plot_(title, file)
