import numpy as np
from collections import OrderedDict


class CentroidTracker:
    """
    Tracks objects across frames by matching centroids by nearest distance.
    Assigns each object a stable integer ID and counts how many frames it
    has been present (used later for loitering).
    """
    def __init__(self, max_disappeared=40, max_distance=80):
        self.next_id = 0
        self.objects = OrderedDict()        # id -> centroid (x, y)
        self.disappeared = OrderedDict()    # id -> frames missing
        self.frames_seen = OrderedDict()    # id -> total frames present
        self.max_disappeared = max_disappeared  # drop after missing this many frames
        self.max_distance = max_distance        # max px to consider "same object"

    def register(self, centroid):
        self.objects[self.next_id] = centroid
        self.disappeared[self.next_id] = 0
        self.frames_seen[self.next_id] = 1
        self.next_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]
        del self.frames_seen[object_id]

    def update(self, rects):
        """
        rects: list of (x1, y1, x2, y2) boxes for this frame.
        Returns dict: id -> (centroid, frames_seen).
        """
        # No detections this frame: mark everyone as disappeared
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self._current_state()

        # Compute centroids of this frame's boxes
        input_centroids = np.zeros((len(rects), 2), dtype="int")
        for i, (x1, y1, x2, y2) in enumerate(rects):
            input_centroids[i] = (int((x1 + x2) / 2.0), int((y1 + y2) / 2.0))

        # No existing objects: register all as new
        if len(self.objects) == 0:
            for c in input_centroids:
                self.register(tuple(c))
            return self._current_state()

        # Match existing objects to new centroids by nearest distance
        object_ids = list(self.objects.keys())
        object_centroids = np.array(list(self.objects.values()))

        # Distance matrix: each existing object vs each new centroid
        D = np.linalg.norm(object_centroids[:, None] - input_centroids[None, :], axis=2)

        rows = D.min(axis=1).argsort()
        cols = D.argmin(axis=1)[rows]

        used_rows, used_cols = set(), set()
        for row, col in zip(rows, cols):
            if row in used_rows or col in used_cols:
                continue
            if D[row, col] > self.max_distance:
                continue
            object_id = object_ids[row]
            self.objects[object_id] = tuple(input_centroids[col])
            self.disappeared[object_id] = 0
            self.frames_seen[object_id] += 1
            used_rows.add(row)
            used_cols.add(col)

        # Existing objects with no match -> disappeared
        unused_rows = set(range(D.shape[0])) - used_rows
        for row in unused_rows:
            object_id = object_ids[row]
            self.disappeared[object_id] += 1
            if self.disappeared[object_id] > self.max_disappeared:
                self.deregister(object_id)

        # New centroids with no match -> register
        unused_cols = set(range(D.shape[1])) - used_cols
        for col in unused_cols:
            self.register(tuple(input_centroids[col]))

        return self._current_state()

    def _current_state(self):
        return {oid: (self.objects[oid], self.frames_seen[oid]) for oid in self.objects}