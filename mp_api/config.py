from loguru import logger

# logger
LOG_LEVEL = "INFO"
LOG_FOLDER = "logs"
LOG_FORMAT = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
              "<level>{level}</level> | "
              "<cyan>{name}</cyan>.<blue>{function}</blue>:     "
              "<level>{message}</level>")

# multi_threading
THREAD_NUM = 16

# tqdm
TQDM_NCOLS = 100
