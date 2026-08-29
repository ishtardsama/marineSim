from dataclasses import dataclass

@dataclass(frozen=True)
class SimConfig:
    #World Dimensions
    worldWidth: int = 1280
    worldHeight: int = 720
    
    #Population
    initialPrey: int = 1500
    
    #Bioenergetics & Thresholds
    baseMetabolism: float = 0.02
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

    #Environmental Grid Parameters
    gridScale: int = 10                     #Each grid cell is 10x10 pixels
    planktonGrowthRate: float = 0.02
    maxPlanktonPerCell: float = 5.0
    biteSize: float = 1.0                   #How much plankton an agent eats per tick
    planktonEnergyMultiplier: float = 15.0  #1 unit of plankton = 15 energy

    #Vision & Steering Parameters
    visionSensorOffsets: tuple = (-0.9, -0.45, 0.0, 0.45, 0.9)  #radians, relative to heading (K=5 sensors)
    visionRangeScale: float = 40.0          #world units of sight per unit of geneVision (0.05-1.0)
    maxTurnRate: float = 0.15               #max radians an agent can turn its heading per tick
    headingNoiseSigma: float = 0.15         #stddev of random heading drift, keeps agents exploring
    headingMutationSigma: float = 0.2       #stddev of heading noise inherited by offspring