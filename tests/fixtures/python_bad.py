import os, sys


def total(values=[]):
  assert values
  try:
    return sum(values)
  except:
    return 0
