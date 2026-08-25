# Marine Life Evolution Engine

A high-performance, Data-Oriented ecosystem simulator built in Python. This engine models emergent natural selection, bioenergetics, and genetic mutation across thousands of autonomous agents in real time using NumPy array vectorization.

## Core Architecture & State

The simulation completely bypasses standard Object-Oriented loops. Instead, it utilizes Data-Oriented Design, storing the ecosystem as massive, parallel NumPy arrays. 

Each agent's physical and biological state is defined by a genetic array, normalized between 0.05 and 1.0:

| Index | Gene | Function in Simulation |
| :--- | :--- | :--- |
| `0` | **Speed** | Dictates pixel velocity and metabolic cost. |
| `1` | **Vision** | (Reserved for future predator/prey detection). |
| `2` | **Thermal** | (Reserved for environmental temperature mapping). |

## Physics and Movement

Agents wander the grid autonomously using vector mathematics. Their velocity is derived directly from their genetic Speed trait, multiplied by a scaling factor to translate it into screen pixels.

*   **Velocity Vector Calculation:**
    Vx = cos(θ) × (G_speed × 3.5)
    Vy = sin(θ) × (G_speed × 3.5)
    
    *(Where θ is a randomly generated heading between 0 and 2π).*

## Bioenergetics and Metabolism

The engine mathematically enforces natural selection by applying a severe trade-off: speed costs energy. Because food is randomly distributed, agents that move unnecessarily fast will rapidly starve.

*   **Metabolic Burn Rate:** Every tick, an agent's energy is reduced by a baseline rate plus a quadratic penalty for its speed.
    E_burn = M_base + 0.5(G_speed)²
    
*   **Foraging Mechanics:** Agents currently operate as passive filter feeders. Every tick, each agent has an 8% probability of finding food, instantly restoring 6.0 energy units.
    
*   **Mortality:** The engine executes a Boolean mask filter every tick. Any agent where E_current ≤ 0 is instantly removed from the arrays.

## Reproduction and Genetic Mutation

Survival of the fittest is modeled via an energy-gated asexual reproduction system. 

*   **Reproduction Trigger:** When an agent accumulates enough food to reach E_current ≥ 90.0, it automatically splits.
*   **Energy Cost:** The parent is immediately taxed 45.0 energy units, and the offspring spawns nearby with a baseline of 40.0 energy units.
*   **Genetic Drift (Mutation):** The offspring inherits the exact DNA array of its parent, modified by random Gaussian noise to simulate mutation.
    G_offspring = max(0.05, min(1.0, G_parent + N(0, σ)))
    
    *(Where σ is the mutation variance of 0.04, applied with a 10% probability per gene).*
