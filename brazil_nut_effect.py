#! /usr/bin/env python3

'''---------------------------------
2-D granular convection simulator

Generates 200 small particles (blue),
and 50 large particles (red) at random
locations in a box subject to gravity
and attempts to simulate granular 
convection.

runs at 240 FPS
scale: 1px = 10cm
speed unit: 1u = 12 ms-1
---------------------------------'''

import pygame
import random
import math

pygame.init()
pygame.display.set_caption("Colliding Particles")

# declare some pygame specific variables

bg_color = (255,255,255)
(width,height) = (200,300)
screen = pygame.display.set_mode((width,height))
screen.fill(bg_color)
clock = pygame.time.Clock()

class Vector:
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length
        
    @property
    def x(self):
        return math.cos(self.angle)*self.length

    @property
    def y(self):
        return math.sin(self.angle)*self.length

    @staticmethod
    def add(vector1, vector2):
        x = vector1.x + vector2.x
        y = vector1.y + vector2.y
        length = math.hypot(x,y)
        angle = math.atan2(y,x)
        return Vector(angle,length)

# Some Constant parameters
gravity = Vector(0.5*math.pi, 0.01)
drag = 0.999
elasticity = 0.50

class Particle:
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.color = (0,0,0)
        self.fillcolor = (4,118,208)
        self.thickness = 1
        self.velocity = Vector(0,1)

    def display(self):
        pygame.draw.circle(screen, self.fillcolor, (self.x, self.y), self.size)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

    def move(self):
        self.velocity = Vector.add(self.velocity, gravity)
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.velocity.length *= drag

# deal with collisions with container walls
    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.velocity.angle = math.pi - self.velocity.angle
            self.velocity.length *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.velocity.angle = math.pi - self.velocity.angle
            self.velocity.length *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.velocity.angle = - self.velocity.angle
            self.velocity.length *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.velocity.angle = - self.velocity.angle
            self.velocity.length *= elasticity

# handle particle-particle collision
def collide(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    distance = math.hypot(dx,dy)

    if distance < p1.size + p2.size:
        normal = math.atan2(dy,dx)
        # angle by which componenets along normal must be flipped
        flipper_angle_1 = normal - 0.5*math.pi - p1.velocity.angle
        flipper_angle_2 = normal - 0.5*math.pi - p2.velocity.angle
        p1.velocity.angle = 2*normal - p1.velocity.angle - math.pi
        p2.velocity.angle = 2*normal - p2.velocity.angle - math.pi

        # correct magnitude of velocities post collision
        (p1.velocity.length, p2.velocity.length) = (math.hypot(math.sin(flipper_angle_2),math.cos(flipper_angle_1)), math.hypot(math.sin(flipper_angle_1),math.cos(flipper_angle_2)))
        p1.velocity.length *= elasticity
        p2.velocity.length *= elasticity

        # particle collision is detected by intersections, so resolve them
        bounce_length = ((p1.size + p2.size) - distance)
        bounce_y = 0.5*bounce_length*math.cos(normal)
        bounce_x = 0.5*bounce_length*math.sin(normal)
        p1.x += bounce_x
        p2.x -= bounce_x
        p1.y -= bounce_y
        p2.y += bounce_y

# Generating random particles
small_particles = 200
big_particles = 50
my_particles=[]

# Generate blue particles of size 5
for i in range(small_particles):
    size = 5
    position = (random.randint(size,width-size), random.randint(size,height-size))
    particle = Particle(position,size)
    particle.velocity.length = random.uniform(0.1,0.2)
    particle.velocity.angle = random.uniform(0.5*math.pi,math.pi)
    my_particles.append(particle)

# Generate red particles of size 10
for i in range(big_particles):
    size = 10 
    position = (random.randint(size,width-size), random.randint(size,height-size))
    particle = Particle(position,size)
    particle.velocity.length = random.uniform(0.1,0.2)
    particle.velocity.angle = random.uniform(0.5*math.pi,math.pi)
    particle.fillcolor=(255,0,0)
    my_particles.append(particle)

def update_screen():
    for i, particle in enumerate(my_particles):
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
    screen.fill(bg_color)
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        particle.display()

paused = False;
running = True
while running:
    pygame.display.flip()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
    update_screen()
    clock.tick(240)
