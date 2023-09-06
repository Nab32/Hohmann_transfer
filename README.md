# Hohmann_transfer
Hohmann Transfer visualization and Mission to Mars

We simulate the Hohmann transfer in the context of our Solar System, where we have a rocket orbiting in Earth's solar orbit that will transfer to Mars' solar orbit.

We split our simulation into two parts:

- Simulating the Hohmann transfer in a two-body context (the Sun and the rocket)
- Simulating a one-way mission of a rocket to Mars
We create a body class with a rocket child class letting us create any planet with n mass and any x-y position. The body class also takes care of all the physics using Newton's laws of gravitation to create our physics engine. The rocket class has additional thrust functions used for the Hohmann transfer. We also have a Python file with all our constants in the International System of Units.

All of our code was written in Python, and we used a library called Pygame for the graphics of our simulation.

2 videos showcasing the simulation:
https://www.youtube.com/watch?v=7dAfUhFeOGc
https://www.youtube.com/watch?v=MROvHgo5GgA&t=1s

