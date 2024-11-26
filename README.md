# Solar system simulator
## Overview
This is a project that I have been workly on for a couple of months. It is a simultation of the solar system that gets initial conditions from NASA's Horizons API and then calculates the trajectories of the planets using Newton's Universal Law of Gravity and his laws of motion. The development of this project was split into 3 versions:
1. The first prototype restricted the solar system to a 2 dimensional plane and didn't take any user inputs.
2. The second version allowed the user to:
   * Scroll in and out (using the scroll wheel)
   * Translate the camera a set distance (by right clicking)
   * Translate the camera so that it followed the planet that was clicked on (by left clicking)
   * Be centred over the centre of mass of the system (by clicking the scroll wheel)
   This version encorporated the third dimension to made calculations more accurate however they still weren't visible
3. The third version allowed the user to:
   * Scroll in and out (using the scroll wheel)
   * Translate the camera (by holding down the left mouse button and moving the mouse)
   * Translate the camera (using the arow keys on the keyboard)
   * Rotate the camera (by holding the right mouse button and moving the mouse)
   * Be centred on a particular planet (by pressing the scroll wheel)

   In addition, it had a second window that allowed the user to:
   * Increase the speed of the simulation
   * Reverse the direction of time
   * Scroll in and out
   * Revert the centre of the camera to the centre of mass
   * View an image and information about the planet that the camera is following (if it is following one)

   This version contained other new features such as the inclusion of moons and a better UI

## Packages
This project mainly uses Pygame - for the simulation. It uses other packages too:

numpy==2.0.1

pillow==11.0.0

pygame==2.6.0

requests==2.32.3

## To do
Ideally I would learn a new compiled language so I could rewrite the code and make it more efficient, however I don't have much experience with packages outside Python so finding an alternative to Pygame may be difficult. Additionally, I want to learn how to implement relativity into this so that the calculations can be more accurate however this will require significantly more computing power due to all the matrices and tensor it will involve.
