#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (C) 2013 Nicolas P. Rougier. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nicolas P. Rougier.
# -----------------------------------------------------------------------------
import os
import numpy as np
import OpenGL.GL as gl
from shader import Shader
from dash_atlas import DashAtlas
from collection import Collection


# -----------------------------------------------------------------------------
class EllipseCollection(Collection):
    # ---------------------------------
    def __init__(self, dash_atlas=None):
        self.vtype = np.dtype([('a_center',   'f4', 2),
                               ('a_texcoord', 'f4', 2)])
        self.utype = np.dtype([('color',     'f4', 4),
                               ('translate', 'f4', 2),
                               ('scale',     'f4', 1),
                               ('rotate',    'f4', 1),
                               ('radius',    'f4', 2),
                               ('linewidth', 'f4', 1),
                               ('antialias', 'f4', 1) ])
        Collection.__init__(self, self.vtype, self.utype)
        if dash_atlas is None:
            self.dash_atlas = DashAtlas()
        else:
            self.dash_atlas = dash_atlas
        shaders = os.path.join(os.path.dirname(__file__),'shaders')
        vertex_shader= os.path.join( shaders, 'ellipses.vert')
        fragment_shader= os.path.join( shaders, 'ellipses.frag')
        self.shader = Shader( open(vertex_shader).read(),
                              open(fragment_shader).read() )


    # ---------------------------------
    def append( self, center=(0, 0), radius=100.0, color=(0, 0, 0, 1),
                linewidth=1.0, antialias=1.0, translate=(0, 0), scale=1.0, rotate=0.0 ):
        V, I, _ = self.bake(center)
        U = np.zeros(1, self.utype)
        U['linewidth'] = linewidth
        U['antialias'] = antialias
        U['color'] = color
        U['translate'] = translate
        U['scale'] = scale
        U['rotate'] = rotate
        U['radius'] = radius
        Collection.append(self, V, I, U)


    # ---------------------------------
    def bake(self, center ):
        V = np.zeros(4, dtype=self.vtype)
        V['a_center'] = center
        V['a_texcoord'] = (-1, -1), (-1, +1), (+1, -1), (+1, +1)
        I = np.array([0, 1, 2, 1, 2, 3], dtype=np.int32)
        return V, I, 0

