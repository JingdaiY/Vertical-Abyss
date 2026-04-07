# PROTOTYPE - NOT FOR PRODUCTION
# Question: Does the core loop of descend -> scavenge -> escape feel engaging?
# Date: 2026-04-07

# 入口点。一切从这里开始，一切也从这里结束。
# The entry point. Everything begins here, and everything ends here.

import pygame
import sys
import os

# Make sure src/ is importable regardless of working directory.
sys.path.insert(0, os.path.dirname(__file__))

from src.game import GameEngine


def main():
    pygame.init()
    pygame.mixer.quit()  # No audio assets yet — skip the mixer to avoid warnings.

    engine = GameEngine()
    engine.run()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
