from extract import extraction
from transform import transform_process
from load import load


def etl_process():
    extraction()
    transform_process().transform()
    load()
    print('ALL DONE')

if __name__ == "__main__":
    etl_process()