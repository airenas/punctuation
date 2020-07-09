import argparse
import sys

import tensorflow as tf

import trainT
####################################################################################
from data import data


####################################################################################
# parameters
####################################################################################
def prepare_train_params(args):
    print("Read Vocab from: ", args.data_dir + "/vocabulary", file=sys.stderr)
    vocab = data.readVocabulary(args.data_dir + "/vocabulary")

    def parse_line_int(t: tf.Tensor):
        return data.parse_simple_line(t, len(data.PUNCTUATION_VOCABULARY))

    strategy = tf.distribute.MirroredStrategy()
    print('Number of devices: %d' % strategy.num_replicas_in_sync, file=sys.stderr)
    batch_size = args.batch_size * strategy.num_replicas_in_sync

    train_file = args.data_dir + "/train"
    print("Setting train data from: ", train_file, file=sys.stderr)
    train_ds = tf.data.TextLineDataset([train_file])
    train_ds = train_ds.map(lambda x: tf.py_function(func=parse_line_int, inp=[x], Tout=[tf.float32, tf.float32]),
                            num_parallel_calls=20)
    train_ds = train_ds.shuffle(args.shuffle)
    train_ds = train_ds.batch(batch_size=batch_size, drop_remainder=True)
    train_ds = train_ds.prefetch(args.prefetch)
    if not (args.prefetch_device is None):
        print("Prefetch to device: ", args.prefetch_device, file=sys.stderr)
        train_ds = train_ds.apply(tf.data.experimental.prefetch_to_device(args.prefetch_device, 5))

    dev_file = args.data_dir + "/dev"
    print("Setting dev data from : ", dev_file, file=sys.stderr)
    dev_ds = tf.data.TextLineDataset([dev_file])
    dev_ds = dev_ds.map(lambda x: tf.py_function(func=parse_line_int, inp=[x], Tout=[tf.float32, tf.float32]),
                        num_parallel_calls=20)
    dev_ds = dev_ds.batch(batch_size=batch_size, drop_remainder=True)
    dev_ds = dev_ds.prefetch(args.prefetch)
    if not (args.prefetch_device is None):
        dev_ds = dev_ds.apply(tf.data.experimental.prefetch_to_device(args.prefetch_device))

    mfp = args.model_dir + "/"
    if args.model_dir is None:
        mfp = ""

    params = trainT.Params(
        vocab=vocab,
        modelFile=mfp + args.prefix + '_{epoch:02d}.h5',
        hidden=args.hidden,
        wordVecSize=args.word_vec_size,
        batchSize=batch_size,
        gpu=args.use_gpu,
        trainSize=data.get_size(args.data_dir + "/train.counts"),
        validationSize=data.get_size(args.data_dir + "/dev.counts"),
        trainData=train_ds,
        validationData=dev_ds,
        strategy=strategy
    )
    return params


def take_cmd_params(argv):
    parser = argparse.ArgumentParser(description="This script trains model with word features",
                                     epilog="E.g. " + sys.argv[0] + " ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--data-dir", default='', type=str, help="Train data directory", required=True)
    parser.add_argument("--model-dir", default='', type=str, help="Model save directory", required=False)
    parser.add_argument("--prefix", default='m1', type=str, help="Output model prefix")
    parser.add_argument("--hidden", default='256', type=int, help="Hidden units in NN layer")
    parser.add_argument("--batch-size", default='128', type=int, help="Batch size")
    parser.add_argument("--shuffle", default='100', type=int, help="Shuffle size")
    parser.add_argument("--prefetch", default='10', type=int, help="Prefetch size")
    parser.add_argument("--prefetch-device", default='', type=str, help="Prefetch device")
    parser.add_argument("--word-vec-size", default='1024', type=int, help="Word vector size")
    parser.add_argument("--use-gpu", action='store_true', help="Use GPU for training")
    args = parser.parse_args(args=argv)
    return args


def main(argv):
    args = take_cmd_params(argv)
    print("Starting", file=sys.stderr)
    params = prepare_train_params(args)
    trainT.trainModel(params)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
