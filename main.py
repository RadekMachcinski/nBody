import numpy as np
import tqdm
import h5py
import random
import scipy.io

class Point:
    def __init__(self, pos, speed, acc = np.array([[0],[0]], dtype = np.float)):
        self.pos = pos
        self.speed = speed
        self.acc = acc
    def step(self, time):
        self.speed += time*self.acc
        self.pos += time*self.speed


def computeAcceleration(arrayOfPoints):
    G = 0.1
    eps = 0.001
    N = len(arrayOfPoints)
    µ = np.ones((N, 1), dtype = np.float)
    r = np.ones((3, N), dtype = np.float)
    for i in arrayOfPoints:
        counter = 0
        for j in arrayOfPoints:
            rij = j.pos - i.pos
            lengthOfrij = np.linalg.norm(rij)
            r[:, counter] = rij[:, 0]
            µ[counter, 0] = 1/(lengthOfrij + eps)**(3/2)
            counter += 1
        i.acc = G*np.dot(r,µ)
    return arrayOfPoints

def frameGenerator(startingState, time):
    state = startingState
    while 1:
        state = computeAcceleration(state)
        for i in state:
            i.step(time)
        yield np.concatenate([x.pos for x in state], axis = 1)

arrOfPoints = []
numberOfPoints = 300
for i in range(0, numberOfPoints):
    arrOfPoints.append(Point(np.array([[random.random()*1000],
                                       [random.random()*1000],
                                       [random.random()*1000]], dtype = np.float),
                                       np.array([[0], [0], [0]], dtype = np.float)))
g = frameGenerator(arrOfPoints, 1)
frames = 1000
mov = np.zeros((3, numberOfPoints, frames), dtype = np.float)
for i in tqdm.tqdm(range(0, frames)):
    mov[: ,: ,i] = next(g)
 #   print(mov[:, :, i])
f = h5py.File("data.hdf5", "w")
f.create_dataset('dataset_1', data=mov)
f.close()
scipy.io.savemat('data.mat', mdict={'data':mov})
