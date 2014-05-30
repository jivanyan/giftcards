import os
import sys

def add_path(rel_path, prepend=False):
  """ 
  Adds a directory to the system python path, either by append (doesn't
  override default or globally installed package names) or by prepend (overrides
  default/global package names).
  """
  path = lambda *paths: os.path.abspath(
      os.path.join(os.path.dirname(__file__), *paths)) + '/'
  if prepend:
    return sys.path.insert(0, path(rel_path))
  return sys.path.append(path(rel_path))

add_path('.')
