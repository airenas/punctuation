import argparse
import sys

import features.features as features
import trainT

####################################################################################
from data import data

minibatches = 128
hidden = 256


####################################################################################
# parameters
####################################################################################
def prepareTrainParams(args):
    print("Read Features from: ", args.data_dir + "/features.txt", file=sys.stderr)
    feat = features.Features(args.data_dir + "/features.txt")

    print("Loading train data: ", args.data_dir + "/train", file=sys.stderr)
    train_data = data.load(args.data_dir + "/train")

    print("Loading validation data: ", args.data_dir + "/dev", file=sys.stderr)
    validation_data = data.load(args.data_dir + "/dev")

    mfp = args.model_dir + "/"
    if args.model_dir is None:
        mfp = ""

    params = trainT.Params(
        trainData=train_data,
        validationData=validation_data,
        modelFile=mfp + args.prefix + '_{epoch:02d}.h5',
        hidden=hidden,
        wordVecSize=hidden,
        minibatches=minibatches,
        gpu=False,
        features=feat
    )
    return params


def takeCmdParams(argv):
    parser = argparse.ArgumentParser(description="This script trains model with word features",
                                     epilog="E.g. " + sys.argv[0] + " ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--data-dir", default='', type=str, help="Train data directory", required=True)
    parser.add_argument("--model-dir", default='', type=str, help="Model save directory", required=False)
    parser.add_argument("--prefix", default='m1', type=str, help="Output model prefix")
    args = parser.parse_args(args=argv)
    return args


def main(argv):
    args = takeCmdParams(argv)
    print("Starting", file=sys.stderr)
    params = prepareTrainParams(args)
    trainT.trainModel(params)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
