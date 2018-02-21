import os

from models.wgancls.model import WGanCls
from models.wgancls.trainer import WGanClsTrainer
from models.wgancls.eval_wgan import WGanClsEval
from utils.utils import pp, show_all_variables
from utils.config import config_from_yaml
from preprocess.dataset import TextDataset

import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_string('cfg', './models/wgancls/cfg/flowers.yml',
                    'Relative path to the config of the model [./models/wgancls/cfg/flowers.yml]')
FLAGS = flags.FLAGS


def main(_):
    pp.pprint(flags.FLAGS.__flags)

    cfg = config_from_yaml(FLAGS.cfg)

    if not os.path.exists(cfg.CHECKPOINT_DIR):
        os.makedirs(cfg.CHECKPOINT_DIR)
    if not os.path.exists(cfg.SAMPLE_DIR):
        os.makedirs(cfg.SAMPLE_DIR)
    if not os.path.exists(cfg.LOGS_DIR):
        os.makedirs(cfg.LOGS_DIR)

    run_config = tf.ConfigProto()
    run_config.gpu_options.allow_growth = True

    datadir = cfg.DATASET_DIR
    dataset = TextDataset(datadir, 299)

    filename_test = '%s/test' % datadir
    dataset._test = dataset.get_data(filename_test)

    filename_train = '%s/train' % datadir
    dataset.train = dataset.get_data(filename_train)

    with tf.Session(config=run_config) as sess:
        if cfg.EVAL.FLAG:
            stage_i = WGanCls(cfg, build_model=False)
            wgan_eval = WGanClsEval(
                sess=sess,
                model=stage_i,
                dataset=dataset,
                cfg=cfg,
            )
            wgan_eval.evaluate()
            return

        if cfg.TRAIN.FLAG:
            stage_i = WGanCls(cfg)
            show_all_variables()
            trainer = WGanClsTrainer(
                sess=sess,
                model=stage_i,
                dataset=dataset,
                cfg=cfg,
            )
            trainer.train()
        else:
            pass


if __name__ == '__main__':
    tf.app.run()
