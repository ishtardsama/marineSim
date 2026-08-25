# Marine Life Evolution Engine

A high-performance, Data-Oriented ecosystem simulator built in Python. This engine models emergent natural selection, bioenergetics, and genetic mutation across thousands of autonomous agents in real time using NumPy array vectorization.

---

## Getting Started

### Prerequisites
You will need Python 3.10+ installed on your system.

### Installation
1. Clone the repository:

        git clone https://github.com/<YOUR-USERNAME>/marine-eco-sim.git
        cd marine-eco-sim

2. Create and activate a virtual environment:

        # Windows
        python -m venv .venv
        .\.venv\Scripts\activate
        
        # macOS/Linux
        python3 -m venv .venv
        source .venv/bin/activate

3. Install the required dependencies:

        pip install -r requirements.txt

### How to Run
Execute the main module from the root directory:

        python -m src.main

---

## Interactive Controls

The viewport features a fully decoupled virtual camera, allowing you to explore the world without affecting the underlying physics engine.

*   **Left Click + Drag:** Pan the camera around the ocean.
*   **Mouse Scroll Wheel:** Zoom in (up to 15x) and zoom out. 
*   **Up Arrow:** Double the simulation speed (1x, 2x, 4x, etc., up to 64x).
*   **Down Arrow:** Halve the simulation speed (minimum 1x).
*   **Spacebar:** Pause/Unpause the physics engine (camera remains active while paused).

---

## Core Architecture & State

Each agent's physical and biological state is defined by a genetic array, normalized between 0.05 and 1.0:

| Index | Gene | Function in Simulation |
| :--- | :--- | :--- |
| `0` | **Speed** | Dictates pixel velocity and metabolic cost (Color: Red = Fast, Blue = Slow). |
| `1` | **Vision** | (Reserved for future predator/prey detection). |
| `2` | **Thermal** | (Reserved for environmental temperature mapping). |

## Physics and Movement

Agents wander the grid autonomously using vector mathematics. Their velocity is derived directly from their genetic Speed trait, multiplied by a scaling factor to translate it into screen pixels.

*   **Velocity Vector Calculation:**
    Vx = cos(θ) × (G_speed × 1.0)
    Vy = sin(θ) × (G_speed × 1.0)
    
    *(Where θ is a randomly generated heading between 0 and 2π).*

## Bioenergetics and Foraging

The engine mathematically enforces natural selection by applying a severe trade-off: speed costs energy. 

*   **Metabolic Burn Rate:** Every tick, an agent's energy is reduced by a baseline rate (`baseMetabolism`) plus a quadratic penalty for its speed.
    E_burn = M_base + 0.5(G_speed)²
    
*   **Spatial Foraging (The Plankton Grid):** Food is not random. The environment is divided into a spatial grid where plankton slowly regrows up to a limit (`maxPlanktonPerCell` = 5.0). Agents take a bite (`biteSize` = 1.0) from the specific cell they are swimming over, mathematically draining that cell's density and instantly restoring their own energy.
    
*   **Mortality:** The engine executes a Boolean mask filter every tick. Any agent where E_current ≤ 0 is instantly removed from the arrays.

## Reproduction and Genetic Mutation

Survival of the fittest is modeled via an energy-gated asexual reproduction system. 

*   **Reproduction Trigger:** When an agent accumulates enough food to reach E_current ≥ 90.0, it automatically splits.
*   **Energy Cost:** The parent is immediately taxed 45.0 energy units, and the offspring spawns nearby with a baseline of 40.0 energy units.
*   **Genetic Drift (Mutation):** The offspring inherits the exact DNA array of its parent, modified by random Gaussian noise to simulate mutation.
    G_offspring = max(0.05, min(1.0, G_parent + N(0, σ)))
    
    *(Where σ is the `mutationSigma` of 0.04, applied with a 10% probability per gene).*

---
*Created as a high-performance Artificial Life exploration.*
