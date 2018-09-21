__author__ = 'tinglev@kth.se'

from modules.util import log
from modules.pipelines.master_pipeline import MasterPipeline

def main():
    log.init_logging()
    pipeline = MasterPipeline()
    pipeline.run_pipeline()

if __name__ == '__main__':
    main()
