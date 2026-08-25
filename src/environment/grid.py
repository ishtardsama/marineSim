import numpy as np
from src.config import SimConfig

class EnvironmentGrid:
    def __init__(self, config: SimConfig):
        self.cfg = config
        #Calculate grid dimensions based on window size and scale
        self.cols = self.cfg.worldWidth // self.cfg.gridScale
        self.rows = self.cfg.worldHeight // self.cfg.gridScale
        
        #Initialize the grid full of plankton
        self.plankton = np.full((self.rows, self.cols), self.cfg.maxPlanktonPerCell, dtype=np.float32)

    def step(self):
        #Slowly regenerate plankton across the entire grid simultaneously
        self.plankton += self.cfg.planktonGrowthRate
        
        #Cap the maximum amount of plankton so it doesn't grow to infinity
        np.clip(self.plankton, 0, self.cfg.maxPlanktonPerCell, out=self.plankton)