# Airdefence Game Documentation

## `MovingObject` Class

This class represents a generic moving object in the game.

### Attributes:

- vx: X-axis velocity.
- vy: Y-axis velocity.
- x: X-coordinate of the object.
- y: Y-coordinate of the object.
- S: Cross-sectional area of the object.
- R: Radius of the object.
- id: Unique identifier for the object.
- air_resistance: Flag indicating whether air resistance is considered.
### Methods:

- update(): Update the object's position and velocity based on physics calculations.


## `Rocket` Class

This class represents a rocket in the game, inheriting from MovingObject.

### Attributes:

- type: String indicating the type of object ("enemy" in this case).
- x1, y1: Target coordinates for the rocket.
- v: Initial velocity of the rocket.
- g: Acceleration due to gravity.
- a0: Initial acceleration of the rocket.
- image: Surface representing the rocket's visual appearance.

### Methods:

- __init__(...): Initialize the rocket object with specific attributes.


## `Bullet` Class
This class represents a bullet in the game, inheriting from MovingObject.

### Attributes:

- type: String indicating the type of object ("bullet" in this case).
- g: Acceleration due to gravity.
- a0: Initial acceleration of the bullet.
- d: Direction of movement.
- rotate: Flag indicating whether the bullet should rotate.
- image: Surface representing the bullet's visual appearance.
### Methods:

- __init__(...): Initialize the bullet object with specific attributes.

## `Wall, Base, Target, and PVO` Classes
These classes represent static objects in the game, inheriting from pygame.sprite.Sprite. They include visual representations and initial positions.


## `Radar` Class
This class represents a radar in the game.

### Attributes:

- x0, y0: Radar's position.
- md: Maximum distance for scanning.

### Methods:

- scan(rockets): Perform a scan on rockets and print the results.
- machine_scan(rockets): Perform a scan on rockets and return the objects.

