from dataclasses import dataclass

@dataclass(frozen=True)
class SimConfig:
    #World Dimensions
    worldWidth: int = 1280
    worldHeight: int = 720
    
    #Population
    initialPrey: int = 1500
    
    #Bioenergetics & Thresholds
    baseMetabolism: float = 0.05
    energyReproductionThreshold: float = 90.0
    energyReproductionCost: float = 45.0
    offspringStartingEnergy: float = 40.0
    maxAgeTicks: int = 2500
    
    #Genetics Index Mapping (DNA columns)
    #the numbers are basically just used as an index to look 
    #up data inside numPy arrays
    geneSpeed: int = 0
    geneVision: int = 1
    geneThermalOpt: int = 2
    numGenes: int = 3
    
    #Evolution Parameters
    mutationRate: float = 0.10
    mutationSigma: float = 0.04