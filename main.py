import asyncio

from src import Simulation, DynamicConfig
from src.visualization import visualize, generate_graphs


async def main():
    loop = asyncio.get_event_loop()

    DynamicConfig.time_modifier = 0.005
    simulation = Simulation(12)

    t1 = loop.create_task(visualize(simulation), name='Visualization')
    t2 = loop.create_task(simulation.run(), name='Simulation')
    t3 = loop.create_task(generate_graphs(simulation), name='Graph Generation')

    await asyncio.gather(t1, t2, t3)


if __name__ == "__main__":
    asyncio.run(main())
