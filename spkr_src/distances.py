__author__ = 'hafiz'
import numpy as np
from scipy.spatial.distance import cosine
class Distance():
    def __init__(self):
        print ''

    def cosine_distance(self,segment):
        row,col = segment.shape

        if row>3:
            angles = np.zeros(row-1)
            for i in range(row)[1:]:
                u = segment[i-1]
                v = segment[i]
                angles[i-1] = np.rad2deg(cosine(u,v))
            return np.mean(angles)
        return -1
    def cosine_distancebetween_segment(self,segment1,segment2):
        # row,col = segment.shape
        return np.rad2deg(cosine(segment1,segment2))
