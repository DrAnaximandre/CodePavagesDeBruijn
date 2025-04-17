import json
import argparse


def define_parser():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Process configuration file.')

    # Add the argument for the config file
    parser.add_argument('-c', '--config', type=str, default='configs/config_polo.json',
                        help='Path to the configuration file')

    # Add the argument for the go function
    parser.add_argument('-g', '--go', type=str, default='goAllDefaults',
                        help='Name of the go function to run')

    parser.add_argument('-N', '--N', type=int, default=5,
                        help='N: lenght of gamma')

    return parser

def get_config():

    parser = define_parser()
    args = parser.parse_args()

    # Load the configuration file
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    # Update the configuration with the command line arguments
    config['Parameters']['N'] = args.N

    return config, args
