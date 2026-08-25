import numpy as np
from src.config import SimConfig

class AgentPopulation:
    def __init__(self, size: int, config: SimConfig):
        self.cfg = config
        
        #State Arrays
        self.positions = np.random.uniform(
            low=[0, 0], 
            high=[config.worldWidth, config.worldHeight], 
            size=(size, 2)
        ).astype(np.float32)
        
        self.velocities = np.zeros((size, 2), dtype=np.float32) #array with 0's
        self.energy = np.full(size, 60.0, dtype=np.float32) 
        self.age = np.zeros(size, dtype=np.int32)
        
        #Genotype Matrix (n agents x numGenes)
        self.dna = np.random.uniform(0.2, 0.8, size=(size, config.numGenes)).astype(np.float32)

    def count(self) -> int:
        return len(self.energy)

    def step(self):
        if self.count() == 0:
            return

        #Physics & Movement
        angles = np.random.uniform(0, 2 * np.pi, size=self.count()).astype(np.float32)
        speeds = (self.dna[:, self.cfg.geneSpeed] * 3.5).astype(np.float32)
        
        self.velocities[:, 0] = np.cos(angles) * speeds
        self.velocities[:, 1] = np.sin(angles) * speeds
        self.positions += self.velocities
        
        #Toroidal wrapping (wrap around screen borders)
        self.positions[:, 0] %= self.cfg.worldWidth
        self.positions[:, 1] %= self.cfg.worldHeight

        #Bioenergetics & Metabolism
        self.age += 1
        speedCost = 0.5 * (self.dna[:, self.cfg.geneSpeed] ** 2)
        metabolicBurn = self.cfg.baseMetabolism + speedCost
        self.energy -= metabolicBurn

        #Foraging chance
        foodFound = np.random.rand(self.count()) < 0.08
        self.energy[foodFound] += 6.0

        #Mortality (Boolean Masking)
        aliveMask = (self.energy > 0) & (self.age < self.cfg.maxAgeTicks)
        self.positions = self.positions[aliveMask]
        self.velocities = self.velocities[aliveMask]
        self.energy = self.energy[aliveMask]
        self.age = self.age[aliveMask]
        self.dna = self.dna[aliveMask]

        #Reproduction & Mutation
        reproduceMask = self.energy >= self.cfg.energyReproductionThreshold
        if np.any(reproduceMask):
            numOffspring = np.sum(reproduceMask)
            self.energy[reproduceMask] -= self.cfg.energyReproductionCost

            parentDna = self.dna[reproduceMask]
            mutation = np.random.normal(0, self.cfg.mutationSigma, size=parentDna.shape).astype(np.float32)
            mutateFlags = np.random.rand(*parentDna.shape) < self.cfg.mutationRate
            
            offspringDNA = np.clip(
                parentDna + (mutation * mutateFlags), 
                0.05, 
                1.0
            ).astype(np.float32)

            offspringPosition = self.positions[reproduceMask] + np.random.uniform(-4, 4, size=(numOffspring, 2))
            offspringPosition[:, 0] %= self.cfg.worldWidth
            offspringPosition[:, 1] %= self.cfg.worldHeight
            
            offspringEnergy = np.full(numOffspring, self.cfg.offspringStartingEnergy, dtype=np.float32)
            offspringAge = np.zeros(numOffspring, dtype=np.int32)
            offspringVelocity = np.zeros((numOffspring, 2), dtype=np.float32)

            self.positions = np.vstack([self.positions, offspringPosition])
            self.velocities = np.vstack([self.velocities, offspringVelocity])
            self.energy = np.concatenate([self.energy, offspringEnergy])
            self.age = np.concatenate([self.age, offspringAge])
            self.dna = np.vstack([self.dna, offspringDNA])