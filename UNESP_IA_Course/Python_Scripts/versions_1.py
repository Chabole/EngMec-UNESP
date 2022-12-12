# -------------------------------------------------------------------
# versions_1.py
# -------------------------------------------------------------------
# Print the versions of Python and the modules/packages used.
# -------------------------------------------------------------------

# -------------------------------------------------------
# Modules to import
# -------------------------------------------------------

import time
import sys
import tensorflow as tf
import numpy as np
import matplotlib as mpl


# -------------------------------------------------------
# def main()
# -------------------------------------------------------

def main():

    print('Test script to identify Python and package/module versions')

    print('---------------------------------------------------')
    print('-- Start script run ' + str(time.strftime('%c')))
    print('-- Python version      : ' + str(sys.version))
    print('-- TensorFlow version  : ' + str(tf.__version__))
    print('-- NumPy version       : ' + str(np.__version__))
    print('-- Matplotlib version  : ' + str(mpl.__version__))
    print('---------------------------------------------------\n')


# -------------------------------------------------------
# Run only if source file is run as the main script
# -------------------------------------------------------

if __name__ == "__main__":

    main()

# -------------------------------------------------------------------
# End of file
# -------------------------------------------------------------------
