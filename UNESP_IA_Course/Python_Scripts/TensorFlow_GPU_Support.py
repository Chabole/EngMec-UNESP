# -------------------------------------------------------------------
# TensorFlow_GPU_Support.py
# -------------------------------------------------------------------
# Identify the number of CPUs and GPUs available on the local
# computer for TensorFlow to access.
# -------------------------------------------------------------------

# -------------------------------------------------------
# Modules to import
# -------------------------------------------------------

import tensorflow as tf
from tensorflow.python.client import device_lib


# -------------------------------------------------------
# def main()
# -------------------------------------------------------

def main():

    print(device_lib.list_local_devices())

    local_devices = tf.config.experimental.list_physical_devices()

    print('Num CPUs Available: ',
          len(tf.config.experimental.list_physical_devices('CPU')))

    for x in local_devices:
        if x.device_type == 'CPU':
            print(x)

    print('Num GPUs Available: ',
          len(tf.config.experimental.list_physical_devices('GPU')))

    for x in local_devices:
        if x.device_type == 'GPU':
            print(x)


if __name__ == "__main__":

    main()

# -------------------------------------------------------------------
# End of file
# -------------------------------------------------------------------
