import sys
import pygame
import numpy as np
from src.config import SimConfig
from src.engine.agents import AgentPopulation

def main():
    pygame.init()
    cfg = SimConfig()
    
    screen = pygame.display.set_mode((cfg.worldWidth, cfg.worldHeight))
    pygame.display.set_caption("Marine Life Evolution Engine - Interactive Camera")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)

    population = AgentPopulation(cfg.initialPrey, cfg)

    #Camera
    running = True
    paused = False
    tick = 0
    cameraPosition = np.array([0.0, 0.0], dtype=np.float32)
    zoom = 1.0
    
    #Panning states
    isPanning = False
    panStartMouse = (0, 0)
    panStartCamera = np.array([0.0, 0.0])
    
    #Simulation Speed (How many ticks to calculate per visual frame)
    simSpeed = 1 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            #KKeyboard controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    simSpeed = min(64, simSpeed * 2) #Double speed (max 64x)
                elif event.key == pygame.K_DOWN:
                    simSpeed = max(1, simSpeed // 2) #Halve speed (min 1x)
                    
            #Mouse controls (zoom and pan)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #Left Click: Start Pan
                    isPanning = True
                    panStartMouse = event.pos
                    panStartCamera = cameraPosition.copy()
                    
                elif event.button == 4 or event.button == 5: #Scroll Wheel
                    #Find world coordinate of screen center before zooming
                    centerWorld = cameraPosition + np.array([cfg.worldWidth/2, cfg.worldHeight/2]) / zoom
                    
                    if event.button == 4: #Scroll Up: Zoom In
                        zoom = min(15.0, zoom * 1.2)
                    elif event.button == 5: #Scroll Down: Zoom Out
                        zoom = max(0.2, zoom / 1.2)
                        
                    #Shift camera so the center of the screen stays the same
                    cameraPosition = centerWorld - np.array([cfg.worldWidth/2, cfg.worldHeight/2]) / zoom

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: #Left Click Release: Stop Pan
                    isPanning = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if isPanning:
                    #Calculate how far mouse moved, divide by zoom so panning feels 1:1
                    dx = event.pos[0] - panStartMouse[0]
                    dy = event.pos[1] - panStartMouse[1]
                    cameraPosition[0] = panStartCamera[0] - (dx / zoom)
                    cameraPosition[1] = panStartCamera[1] - (dy / zoom)

        #Physics engine (Runs multiple times based on simSpeed)
        if not paused:
            for _ in range(simSpeed):
                population.step()
                tick += 1

        # Render virtual camera
        screen.fill((10, 20, 35)) 

        if population.count() > 0:
            #Transform all world coordinates to screen coordinates instantly with NumPy
            screenCoords = ((population.positions - cameraPosition) * zoom).astype(np.int32)
            
            #Scale agent size based on zoom (minimum 1 pixel)
            agentSize = max(1, int(zoom))
            
            #Colors: red
            speedGene = population.dna[:, cfg.geneSpeed]
            r = (speedGene * 255).astype(np.uint8)
            g = (150 * (1 - speedGene)).astype(np.uint8)
            b = (255 * (1 - speedGene)).astype(np.uint8)

            for i in range(population.count()):
                #Screen Culling: this only draw agents that are actually visible on screen
                sx, sy = screenCoords[i, 0], screenCoords[i, 1]
                if -agentSize <= sx <= cfg.worldWidth and -agentSize <= sy <= cfg.worldHeight:
                    pygame.draw.rect(screen, (r[i], g[i], b[i]), (sx, sy, agentSize, agentSize))

            #Telemetry logic
            avgSpeed = np.mean(speedGene)
            avgEnergy = np.mean(population.energy)
            stats = [
                f"Tick: {tick}",
                f"Population: {population.count()}",
                f"Avg Speed Gene: {avgSpeed:.3f}",
                f"Avg Energy: {avgEnergy:.1f}",
                f"Zoom(scrollwheel): {zoom:.2f}x",
                f"Speed(↑ & ↓ to change): {simSpeed}x {'(PAUSED)' if paused else ''}",
                f"FPS: {clock.get_fps():.0f}"
            ]
        else:
            stats = [f"Tick: {tick}", "EXTINCT", f"Zoom: {zoom:.2f}x", f"FPS: {clock.get_fps():.0f}"]

        #Draw HUD text
        for idx, text in enumerate(stats):
            surf = font.render(text, True, (220, 220, 220))
            screen.blit(surf, (10, 10 + idx * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()