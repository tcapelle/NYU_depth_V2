# AUTOGENERATED! DO NOT EDIT! File to edit: 00_utils.ipynb (unless otherwise specified).

__all__ = ['to_viridis', 'show_image', 'show_images']

# Cell
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from fastcore.all import *

# Cell
def _scale_image(img:np.ndarray, high=1.):
    return (img-img.min())/(img.max()-img.min())*high

def _format_tensor_array(im):
    # Handle pytorch axis order
    if not isinstance(im,np.ndarray):
        im = np.array(im)
    # Handle 1-channel images
    if im.shape[-1]==1:
        im = im[...,0]
    return im

# Cell
def to_viridis(tensor_image):
    image_array = _format_tensor_array(tensor_image)
    image_array = _scale_image(image_array, high=1)
    return Image.fromarray(np.uint8(cm.viridis(image_array)*255))

# Cell

# This comes from fastai.torch_core

def _fig_bounds(x):
    r = x//32
    return min(5, max(1,r))

@delegates(plt.Axes.imshow, keep=True, but=['shape', 'imlim'])
def show_image(im, ax=None, figsize=None, title=None, ctx=None, **kwargs):
    "Show a PIL or PyTorch image on `ax`."
    im = _format_tensor_array(im)

    ax = ifnone(ax,ctx)
    if figsize is None: figsize = (_fig_bounds(im.shape[0]), _fig_bounds(im.shape[1]))
    if ax is None: _,ax = plt.subplots(figsize=figsize)
    ax.imshow(im, **kwargs)
    if title is not None: ax.set_title(title)
    ax.axis('off')
    return ax

@delegates(plt.subplots)
def show_images(ims, nrows=1, ncols=None, titles=None, **kwargs):
    "Show all images `ims` as subplots with `rows` using `titles`."
    if ncols is None: ncols = int(math.ceil(len(ims)/nrows))
    if titles is None: titles = [None]*len(ims)
    axs = plt.subplots(nrows, ncols, **kwargs)[1].flat
    for im,t,ax in zip(ims, titles, axs): show_image(im, ax=ax, title=t)