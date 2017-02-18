#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
#

import os
import sys
import math
import numpy as np
import cntk as ct

def build_model(num_classes, model_name):
    '''
    Factory function to instantiate the model.
    '''
    model = getattr(sys.modules[__name__], model_name)
    return model(num_classes)

class VGG13(object):
    '''
    A VGG13 like model (https://arxiv.org/pdf/1409.1556.pdf) tweaked for emotion data.
    '''
    @property
    def learning_rate(self):
        return 0.05

    @property
    def input_width(self):
        return 64

    @property
    def input_height(self):
        return 64

    @property
    def input_channels(self):
        return 1

    @property
    def model(self):
        return None

    @property
    def model(self):
        return self._model

    def __init__(self, num_classes):
        self._model = self._create_model(num_classes)

    def _create_model(self, num_classes):
        with ct.default_options(activation=ct.relu, init=ct.glorot_uniform()):
            model = ct.Sequential([
                ct.For(range(2), lambda i: [
                    ct.Convolution((3,3), [64,128][i], pad=True),
                    ct.Convolution((3,3), [64,128][i], pad=True),
                    ct.MaxPooling((2,2), strides=(2,2)),
                    ct.Dropout(0.25)
                ]),
                ct.For(range(2), lambda i: [
                    ct.Convolution((3,3), [256,256][i], pad=True),
                    ct.Convolution((3,3), [256,256][i], pad=True),
                    ct.Convolution((3,3), [256,256][i], pad=True),                
                    ct.MaxPooling((2,2), strides=(2,2)),
                    ct.Dropout(0.25)
                ]),            
                ct.For(range(2), lambda : [
                    ct.Dense(1024),
                    ct.Dropout(0.5)
                ]),
                ct.Dense(num_classes, activation=None)
            ])
        return model
