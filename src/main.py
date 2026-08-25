import sys
import pygame
import numpy as np
from src.config import SimConfig
from src.engine.agents import AgentPopulation

def main():
    pygame.init()
    cfg = SimConfig()
    
    screen = pygame.display.set_mode((cfg.worldWidth, cfg.worldHeight))
    pygame.display.set_caption("MarineSim (v1.0)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)

    population = AgentPopulation(cfg.initialPrey, cfg)
    running = True
    tick = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        population.step()
        tick += 1

        screen.fill((10, 20, 35))  # Deep ocean navy

        if population.count() > 0:
            coords = population.positions.astype(np.int32)
            
            #Red = Fast gene, Blue = Slow gene
            speedGene = population.dna[:, cfg.geneSpeed]
            r = (speedGene * 255).astype(np.uint8)
            g = (150 * (1 - speedGene)).astype(np.uint8)
            b = (255 * (1 - speedGene)).astype(np.uint8)

            for i in range(population.count()):
                screen.set_at((coords[i, 0], coords[i, 1]), (r[i], g[i], b[i]))

            avgSpeed = np.mean(speedGene)
            avgEnergy = np.mean(population.energy)
            stats = [
                f"Tick: {tick}",
                f"Population: {population.count()}",
                f"Avg Speed Gene: {avgSpeed:.3f}",
                f"Avg Energy: {avgEnergy:.1f}",
                f"FPS: {clock.get_fps():.0f}"
            ]
        else:
            stats = [f"Tick: {tick}", "POPULATION EXTINCT", f"FPS: {clock.get_fps():.0f}"]

        for idx, text in enumerate(stats):
            surf = font.render(text, True, (220, 220, 220))
            screen.blit(surf, (10, 10 + idx * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()