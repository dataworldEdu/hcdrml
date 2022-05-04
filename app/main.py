import argparse
from fastcore.transform import Pipeline
from .data import ingestion, preprocessing
from .model import lightgbm

parser = argparse.ArgumentParser
parser.add_argument('-s', '--start', help="Start Pipline Flow")
parser.add_argument('-e', '--end', help='End Pipeline Flow')
parser.add_argument('-t', '--test', help='Model Test')
parser.add_argument('-m', '--model', help="Model File")

args = parser.parse_args()


def main():
    all_flow_list = [
        ingestion.get_data,
        preprocessing.nvl,
        preprocessing.one_hot_encoding,
        preprocessing.min_max_scale,
        lightgbm.run,
        lightgbm.print_metric_score,
        lightgbm.model_predict,
    ]

    if args.start:
        if args.start == 'ing':
            ...

        elif args.start == 'prep':
            ...

        elif args.start == 'model':
            ...

    if args.end:
        if args.end == 'prep':
            ...
        elif args.end == 'model':
            ...

    if args.test:
        if args.model:
            ...
        else:
            raise Exception

    pipe = Pipeline(all_flow_list)
    pipe()


if __name__ == '__main__':
    main()
