import argparse

from engine.colab.RunColab import run_colab

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Train Persona')
    parser.add_argument('--persona', required=True, help='persona name')
    parser.add_argument('--engine', required=True, help='run engine type')
    args = parser.parse_args()
    if args.engine == 'colab':
        run_colab(args.persona)
    else:
        print('Engine type not supported: ', args.engine)
