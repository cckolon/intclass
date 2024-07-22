import argparse

from data_generation.make_training_data import make_training_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_rows", type=int)
    args = parser.parse_args()
    make_training_data(args.num_rows)
