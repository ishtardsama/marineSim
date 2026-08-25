import sys
import pygame
import numpy as np
from src.config import SimConfig
from src.engine.agents import AgentPopulation
from src.environment.grid import EnvironmentGrid 

def main():
    pygame.init()
    cfg = SimConfig()
    
    screen = pygame.display.set_mode((cfg.worldWidth, cfg.worldHeight))
    pygame.display.set_caption("Marine Life Evolution Engine")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 15)

    population = AgentPopulation(cfg.initialPrey, cfg)
    environment = EnvironmentGrid(cfg) #Initialize grid
    
    running = True
    paused = False
    tick = 0
    
    cameraPosition = np.array([0.0, 0.0], dtype=np.float32)
    zoom = 1.0
    isPanning = False
    panStartMouse = (0, 0)
    panStartCamera = np.array([0.0, 0.0])
    simSpeed = 1 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    simSpeed = min(64, simSpeed * 2)
                elif event.key == pygame.K_DOWN:
                    simSpeed = max(1, simSpeed // 2)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    isPanning = True
                    panStartMouse = event.pos
                    panStartCamera = cameraPosition.copy()
                elif event.button == 4 or event.button == 5: 
                    centerWorld = cameraPosition + np.array([cfg.worldWidth/2, cfg.worldHeight/2]) / zoom
                    if event.button == 4: 
                        zoom = min(15.0, zoom * 1.2)
                    elif event.button == 5: 
                        zoom = max(0.2, zoom / 1.2)
                    cameraPosition = centerWorld - np.array([cfg.worldWidth/2, cfg.worldHeight/2]) / zoom

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    isPanning = False
            elif event.type == pygame.MOUSEMOTION:
                if isPanning:
                    dx = event.pos[0] - panStartMouse[0]
                    dy = event.pos[1] - panStartMouse[1]
                    cameraPosition[0] = panStartCamera[0] - (dx / zoom)
                    cameraPosition[1] = panStartCamera[1] - (dy / zoom)

        #Physics engine
        if not paused:
            for _ in range(simSpeed):
                environment.step() #Grow plankton
                population.step(environment) # Pass grid to agents
                tick += 1

        #Render virtual camera
        screen.fill((10, 20, 35)) 

        #Plankton grid render w screen culling
        #Base RGB matrix
        colorMatrix = np.zeros((environment.cols, environment.rows, 3), dtype=np.uint8)
        greenIntensity = (environment.plankton.T / cfg.maxPlanktonPerCell * 120).astype(np.uint8)
        colorMatrix[:, :, 1] = greenIntensity 
        colorMatrix[:, :, 0] = 10 
        colorMatrix[:, :, 2] = 35 

        #Find exact grid columns/rows visible on screen
        colStart = int(max(0, cameraPosition[0] / cfg.gridScale))
        colEnd = int(min(environment.cols, (cameraPosition[0] + cfg.worldWidth / zoom) / cfg.gridScale + 1))
            
        rowStart = int(max(0, cameraPosition[1] / cfg.gridScale))
        rowEnd = int(min(environment.rows, (cameraPosition[1] + cfg.worldHeight / zoom) / cfg.gridScale + 1))

        #Slice the matrix (crop it) and scale ONLY the visible portion
        if colStart < colEnd and rowStart < rowEnd:
            visibleMatrix = colorMatrix[colStart:colEnd, rowStart:rowEnd]
            gridSurf = pygame.surfarray.make_surface(visibleMatrix)
                
            #Scale the tiny cropped surface to fit the screen
            scaledWidth = int((colEnd - colStart) * cfg.gridScale * zoom)
            scaledHeight = int((rowEnd - rowStart) * cfg.gridScale * zoom)
                
            if scaledWidth > 0 and scaledHeight > 0:
                gridSurf = pygame.transform.scale(gridSurf, (scaledWidth, scaledHeight))
                    
                #Calculate sub-pixel offset so it pans smoothly
                screenX = int((colStart * cfg.gridScale - cameraPosition[0]) * zoom)
                screenY = int((rowStart * cfg.gridScale - cameraPosition[1]) * zoom)
                    
                screen.blit(gridSurf, (screenX, screenY))

        if population.count() > 0:
            screenCoords = ((population.positions - cameraPosition) * zoom).astype(np.int32)
            agentSize = max(1, int(zoom))
            
            speedGene = population.dna[:, cfg.geneSpeed]
            r = (speedGene * 255).astype(np.uint8)
            g = (150 * (1 - speedGene)).astype(np.uint8)
            b = (255 * (1 - speedGene)).astype(np.uint8)

            for i in range(population.count()):
                sx, sy = screenCoords[i, 0], screenCoords[i, 1]
                if -agentSize <= sx <= cfg.worldWidth and -agentSize <= sy <= cfg.worldHeight:
                    pygame.draw.rect(screen, (r[i], g[i], b[i]), (sx, sy, agentSize, agentSize))

            avgSpeed = np.mean(speedGene)
            avgEnergy = np.mean(population.energy)
            stats = [
                f"Tick: {tick}",
                f"Population: {population.count()}",
                f"Avg Speed Gene: {avgSpeed:.3f}",
                f"Avg Energy: {avgEnergy:.1f}",
                f"Zoom: {zoom:.2f}x",
                f"Speed: {simSpeed}x {'(PAUSED)' if paused else ''}",
                f"FPS: {clock.get_fps():.0f}"
            ]
        else:
            stats = [f"Tick: {tick}", "EXTINCT", f"Zoom: {zoom:.2f}x", f"FPS: {clock.get_fps():.0f}"]

        for idx, text in enumerate(stats):
            surf = font.render(text, True, (220, 220, 220))
            screen.blit(surf, (10, 10 + idx * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()