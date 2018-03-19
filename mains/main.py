from utils.notebook_util import setup_one_gpu
setup_one_gpu()

import tensorflow as tf

from data_loader.data_generator import DataGenerator
from models.model import Model
from trainers.trainer import Trainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.logger import Logger
from utils.utils import get_args


def main():
  # capture the config path from the run arguments
  # then process the json configuration file
  try:
    args = get_args()
    config = process_config(args.config)
    print(config)
  except:
    print("missing or invalid arguments")
    exit(0)

  # create the experiments dirs
  create_dirs([config.summary_dir, config.checkpoint_dir])
  # create tensorflow session
  sess = tf.Session()
  # create an instance of the model you want
  model = Model(config)
  # load model if exists
  model.load(sess)
  # create your data generator
  data = DataGenerator(config)
  # create tensorboard logger
  logger = Logger(sess, config)
  # create trainer and pass all the previous components to it
  trainer = Trainer(sess, model, data, config, logger)

  # here you train your model
  trainer.train()


if __name__ == '__main__':
  main()