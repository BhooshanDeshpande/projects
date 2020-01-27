# agent.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Clemson University and the author.
#
# Author: Ioannis Karamouzas (ioannis@g.clemson.edu)
#  ================================================================
import numpy as np
from math import sqrt
import math

def mag(x):
    return math.sqrt(sum(i ** 2 for i in x))

def get_optimal_velocity(costs=[], velocities=[]):
    min_cost = min(costs)
    index = costs.index(min_cost)
    optimal_velocity = velocities[index]
    return optimal_velocity

class Agent(object):
    pi = 3.14

    def __init__(self, csvParameters, dhor=5, goalRadiusSq=1):
        colors = ["#FAA", "blue", "yellow", "white"]  # agent colors
        self.id = int(csvParameters[0])  # the id of the agent
        self.gid = int(csvParameters[1])  # the group id of the agent
        self.pos = np.array([float(csvParameters[2]), float(csvParameters[3])])  # the position of the agent
        self.vel = np.zeros(2)  # the velocity of the agent
        self.goal = np.array([float(csvParameters[4]), float(csvParameters[5])])  # the goal of the agent
        self.prefspeed = float(csvParameters[6])  # the preferred speed of the agent
        self.gvel = self.goal - self.pos  # the goal velocity of the agent
        self.gvel = self.gvel / (sqrt(self.gvel.dot(self.gvel))) * self.prefspeed
        self.maxspeed = float(csvParameters[7])  # the maximum sped of the agent
        self.radius = float(csvParameters[8])  # the radius of the agent
        self.goalRadiusSq = goalRadiusSq  # parameter to determine if agent is close to the goal
        self.atGoal = False  # has the agent reached its goal?
        self.dhor = dhor  # the sensing radius
        self.vnew = np.zeros(2)  # the new velocity of the agent
        self.vcand = np.zeros(2)
        self.color = colors[self.gid % 4]

    def ttc(self, closest_neighbor):
        if not closest_neighbor:
            return float('inf')
        else:
            rad = self.radius + closest_neighbor.radius
            w = self.pos - closest_neighbor.pos
            c = w.dot(w) - rad * rad  # agents are colliding
            if c < 0:
                return 0
            v = self.vcand - closest_neighbor.vel
            a = v.dot(v)
            b = w.dot(v)
            if b > 0:  # agents are diverging
                return float('inf')
            discr = b * b - a * c
            if discr <= 0:
                return float('inf')
            tau = c / (-b + sqrt(discr))  # smallest root
            if tau < 0:
                return float('inf')
            return tau

    def check_nearest_neighbor_in(self, neighbors):
        nearest_neighbors = []
        distances = []
        if not neighbors:
            print('No neighbors in the scenario!!')
            pass
        else:
            for neighbor in neighbors:
                x1 = neighbor.pos[0]
                y1 = neighbor.pos[1]
                x2 = self.pos[0]
                y2 = self.pos[1]
                distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                if 0.99999 * (self.radius + neighbor.radius) <= distance <= 1.0001 * (self.radius + neighbor.radius):
                    closest_neighbor = neighbor
                else:
                    if distance <= self.dhor and neighbor is not self:
                        nearest_neighbors.append(neighbor)
                        distances.append(distance)
                    if not distances:
                        pass
                    else:
                        closest_neighbor = nearest_neighbors[distances.index(min(distances))]
            if not nearest_neighbors:
                nearest_neighbors = []
                closest_neighbor = []
                return nearest_neighbors, closest_neighbor
            else:
                return nearest_neighbors, closest_neighbor

    def get_distance(self,closest_neighbor):
        if not closest_neighbor:
            return float('inf')
        else:
            x1 = closest_neighbor.pos[0]
            y1 = closest_neighbor.pos[1]
            x2 = self.pos[0]
            y2 = self.pos[1]
            distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            return distance

    def computeNewVelocity(self, neighbors):
        sensed_neighbors, closest_neighbor = self.check_nearest_neighbor_in(neighbors)
        samples = 100
        costs = []
        velocities = []
        for i in range(samples):
            # sampling velocities in a random fashion
            sample_angles = np.random.random_sample() * 2 * Agent.pi
            sample_radius = np.random.random_sample() * self.maxspeed * sqrt(np.random.random_sample())
            sample_x = sample_radius * math.cos(sample_angles)
            sample_y = sample_radius * math.sin(sample_angles)
            self.vcand = [sample_x, sample_y]
            velocities.append(self.vcand)
            tau = self.ttc(closest_neighbor)
            if len(neighbors) == 3:
                alpha = 7
                beta = 11
                gamma = 17
            if len(neighbors) == 8:
                alpha = 8
                beta = 12
                gamma = 30
            if len(neighbors) == 40:
                alpha =8
                beta = 22
                gamma = 40
            costs.append(alpha * mag(self.vcand - self.gvel) + beta * mag(self.vcand - self.vel) + gamma / (10e-200 + tau))
            optimal_velocity = get_optimal_velocity(costs, velocities)
        if self.atGoal:
            self.vnew[:] = np.zeros(2)
        else:
            self.vnew[:] = optimal_velocity[:]

    def update(self, dt):
        if not self.atGoal:
            self.vel[:] = self.vnew[:]
            self.pos += self.vel * dt  # update the position

            # compute the goal velocity for the next time step. Do not modify this
            self.gvel = self.goal - self.pos
            distGoalSq = self.gvel.dot(self.gvel)
            if distGoalSq < self.goalRadiusSq:
                self.atGoal = True  # goal has been reached
            else:
                self.gvel = self.gvel / sqrt(distGoalSq) * self.prefspeed
