#!/usr/bin/env python3

import math

def distance(a: tuple[float, float], b: tuple[float, float]) -> float: 
  return math.sqrt(abs(a[0] - b[0])**2 + abs(a[1] - b[1])**2)
