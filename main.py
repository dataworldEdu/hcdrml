import argparse
from fastcore.transform import Pipeline
from app.data import ingestion, preprocessing
from app.model import lightgbm

parser = argparse.ArgumentParser(description='Python ML App')
parser.add_argument('-o', '--only', help='Only one process execute')
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

    if args.only:
        if args.only == 'ing':
            all_flow_list = [ingestion.get_data]

    elif args.start:
        if args.start == 'ing':
            ...

        elif args.start == 'prep':
            ...

        elif args.start == 'model':
            ...

    elif args.end:
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
    pipe(1)


if __name__ == '__main__':
    main()
