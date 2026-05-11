"""Utilities and helpers"""
import json
import numpy as np
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.generic):
            return obj.item()
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def encode_response(data):
    """Encode response data"""
    return json.loads(json.dumps(data, cls=JSONEncoder))
