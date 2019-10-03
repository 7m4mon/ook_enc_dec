#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 7M4MON
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

"""=================================================="""
"""          Super Hikari Mascon Decoder             """
"""                               2019.Sep.30 7M4MON """
"""=================================================="""

import numpy
import math
from gnuradio import gr

class masdec_ii(gr.sync_block):
    """
    docstring for block masdec_ii
    """
    def __init__(self, thres_duration, max_state):
        gr.sync_block.__init__(self,
            name="masdec_ii",
            in_sig=[numpy.int32],
            out_sig=[numpy.int32])
        self.on_counter = 0
        self.last_count = 0
        self.last_bit = 0
        self.thres_duration = thres_duration
        self.limit = thres_duration * (max_state + 1) - 1



    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        for det_bit in in0:
            if det_bit == 1 :
                self.on_counter += 1
                if self.on_counter > self.limit : self.on_counter = self.limit
            else :
                if self.last_bit == 1 :    # edge 1 -> 0
                    self.last_count = self.on_counter
                self.on_counter = 0    # clear counter
            
            self.last_bit = det_bit
            
        out[:] = math.floor(self.last_count / self.thres_duration)
        
        return len(output_items[0])


