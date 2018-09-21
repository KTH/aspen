__author__ = 'tinglev@kth.se'

import time
from modules.util import log
from modules.pipelines.master_pipeline import MasterPipeline

def main():
    log.init_logging()
    pipeline = MasterPipeline()
    while True:
        pipeline.run_pipeline()
        time.sleep(15)

if __name__ == '__main__':
    main()
