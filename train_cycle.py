from dual_network import dual_network
from self_play import self_play
from train_network import train_network
import tensorflow as tf
#from evaluate_best_player import evaluate_best_player

dual_network()
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024 * 6)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)
for i in range(1000) : 
    print('Train', i, '======================')

    self_play()

    train_network()

    #evaluate_best_player()