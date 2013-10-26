import logging

logging.basicConfig(format = "[%(asctime)s] %(filename)s[line:%(lineno)d] : [%(levelname)s] %(message)s", level = logging.DEBUG)


if __name__ == "__main__":
    logging.debug("11")
