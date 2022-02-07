import os

SUPPORTED_SIZE        = int(os.environ["SUPPORTED_SIZE"])
SUPPORTED_WIDTH       = int(os.environ["SUPPORTED_RESOLUTION"].split("x")[0])
SUPPORTED_HEIGTH      = int(os.environ["SUPPORTED_RESOLUTION"].split("x")[1])
CONDITION_TO_VALIDATE = os.environ["CONDITION_TO_VALIDATE"]