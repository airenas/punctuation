import argparse
import sys

import model.model as model


def show_info(args):
    print('Loading', file=sys.stderr)
    m = model.load(args.model)
    m.summary(150)
    print('Params:')
    print('Input name  :', m.input.name)
    print('Output name :', m.output.name)


def take_cmd_params(argv):
    parser = argparse.ArgumentParser(
        description="This script writes model structure",
        epilog="E.g. " + sys.argv[0] + "",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("model", type=str, help="Model file", required=True)
    args = parser.parse_args(args=argv)
    return args


def main(argv):
    print("Starting", file=sys.stderr)
    args = take_cmd_params(argv)
    show_info(args)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
