from distutils.core import setup
from Cython.Build import cythonize
 
setup(
  name = 'pack1',
  ext_modules = cythonize(["GOP3blackjack.py",]
  ),
)