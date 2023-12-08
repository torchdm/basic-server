import yaml
from Inc.SerMain import *
import os

config = yaml.safe_load(open("config.yml"))

TorchSessionController = TSC()
for i in os.listdir("kexts"):
    if i.endswith(".py"):
        print(f"KEXT IMPORT {i}")
        TorchSessionController.add_extension(f"kexts.{i[:-3]}")

TorchSessionController.serve_forever(config)
