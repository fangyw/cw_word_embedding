# -*- coding: utf-8 -*-
__author__ = 'klb3713'


import math
import numpy

import config
import vocabulary

sqrt3 = math.sqrt(3.0)


def random_weights(nin, nout, scale_by=1./sqrt3, power=0.5):
    return (numpy.random.rand(nin, nout) * 2.0 - 1) * scale_by * sqrt3 / pow(nin, power)


class Parameters:
    """
    Parameters used by the L{Model}.
    @todo: Document these
    """

    def __init__(self, window_size=config.WINDOW_SIZE,
                 embedding_size=config.EMBEDDING_SIZE, hidden_size=config.HIDDEN_SIZE):
        """
        Initialize L{Model} parameters.
        """

        self.vocab_size = vocabulary.length()
        self.window_size = window_size
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.output_size = 1
        self.input_size = self.embedding_size * self.window_size

        numpy.random.seed()

        self.embeddings = (numpy.random.rand(self.vocab_size, self.embedding_size) - 0.5) * 2
        if config.NORMALIZE_EMBEDDINGS:
            self.normalize(range(self.vocab_size))

        self.hidden_weights = random_weights(self.input_size, self.hidden_size, scale_by=config.SCALE_INITIAL_WEIGHTS_BY)
        self.output_weights = random_weights(self.hidden_size, self.output_size, scale_by=config.SCALE_INITIAL_WEIGHTS_BY)
        self.hidden_biases = numpy.zeros((1, self.hidden_size))
        self.output_biases = numpy.zeros((1, self.output_size))

    def normalize(self, indices):
        """
        Normalize such that the l2 norm of the embeddings indices passed in.
        @todo: l1 norm?
        @return: The normalized embeddings
        """
        l2norm = numpy.square(self.embeddings[indices]).sum(axis=1)
        l2norm = numpy.sqrt(l2norm.reshape((len(indices), 1)))

        self.embeddings[indices] /= l2norm
        self.embeddings[indices] *= math.sqrt(self.embeddings.shape[1])
