import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class new_ball:
    def __init__(self, x, y, u, v):
        self.location = [x,y]
        self.velocity = [u,v]
        self.next_location = [0,0]
        self.next_velocity = [0,0]

def linear_motion(location, velocity, dt):
    return (location[0]+dt*velocity[0], location[1]+dt*velocity[1])

def ball_loc():
    x_locs = [[],[]]
    y_locs = [[],[]]
    t = 0
    t_final = 50
    dt = 0.02
    r = 0.05
    balls = [new_ball(0.75, 5*r, -0.1, 0.5), new_ball(0.25, 5.5*r, 0.11, 0.2)]
    alpha = 0.8
    beta = 0.98
    while t < t_final:
        collision = [-1, -1]
        #calculate theoretical location with linear motion
        for ball in balls:
            ball.next_location = (linear_motion(ball.location, ball.velocity, dt))
            ball.next_velocity = ball.velocity
    
        #first, we will find the smallest dt based on all wall and ball collisions
        counter = 0
        smallest_dt = dt
        for ball in balls:
            #check right wall
            if ball.next_location[0]+r > 1:
                dt_new = abs((1-(ball.location[0]+r))/ball.velocity[0])
                if smallest_dt > dt_new:
                    smallest_dt = dt_new
                    collision = [counter, 0]
            #left wall
            if ball.next_location[0]-r < 0:
                dt_new = abs((-(ball.location[0]-r))/ball.velocity[0])
                if smallest_dt > dt_new:
                    smallest_dt = dt_new
                    collision = [counter, 0]
            #top wall
            if ball.next_location[1]+r > 1:
                dt_new = abs((1-(ball.location[1]+r))/ball.velocity[1])
                if smallest_dt > dt_new:
                    smallest_dt = dt_new
                    collision = [counter, 1]
            #bottom wall
            if ball.next_location[1]-r < 0:
                dt_new = abs((-(ball.location[1]-r))/ball.velocity[1])
                if smallest_dt > dt_new:
                    smallest_dt = dt_new
                    collision = [counter, 1]
            counter += 1
        #ball collision with the other ball
        #make everything into numpy arrays to take advantage of np's built in norm function
        ball0_vel = np.array(balls[0].velocity)
        ball1_vel = np.array(balls[1].velocity)
        ball0_pos = np.array(balls[0].next_location)
        ball1_pos = np.array(balls[1].next_location)
        rel_vel = np.linalg.norm(ball0_vel - ball1_vel)
        rel_pos = np.linalg.norm(ball0_pos - ball1_pos)
    
        #Detect a ball-ball collision
        if rel_pos < 2*r:
            dt_new = abs((rel_pos-2*r)/rel_vel)
            if smallest_dt > dt_new:
                smallest_dt = dt_new
                collision = [-1, 2]    

        #There was a collision at some point (smallest_dt < dt)
        if smallest_dt < dt:
            for ball in balls:
                ball.next_location = (linear_motion(ball.location, ball.velocity, smallest_dt))
            collision_type = collision[1]
            old_vel = balls[collision[0]].velocity
            if collision_type == 0:
                balls[collision[0]].next_velocity = [-alpha * old_vel[0], beta * old_vel[1]]
            elif collision_type == 1:
                balls[collision[0]].next_velocity = [beta * old_vel[0], -alpha * old_vel[1]]
            elif collision_type == 2:
                rel_pos = ball0_pos - ball1_pos
                rel_vel = ball0_vel - ball1_vel
                n = rel_pos / np.sqrt(np.sum(rel_pos**2))
                delta = np.array([n[1], -n[0]])
                balls[0].next_velocity = (np.dot(ball1_vel, n)*n + np.dot(ball0_vel, delta)*delta).tolist()
                balls[1].next_velocity = (np.dot(ball0_vel, n)*n + np.dot(ball1_vel, delta)*delta).tolist()

        #The next_velocities have all been set, time to update the balls for the next tick
        for i in range(len(balls)):
            balls[i].velocity = balls[i].next_velocity
            balls[i].location = balls[i].next_location
            x_locs[i].append(balls[i].location[0])
            y_locs[i].append(balls[i].location[1])
        
        t += smallest_dt

    return x_locs, y_locs
# function that draws each frame of the animation
def animate(i):
    r = 0.05
    ax.clear()
    ax.set_aspect(1)
    circle1 = plt.Circle((x_animation[0][i], y_animation[0][i]), r, color="red")
    circle2 = plt.Circle((x_animation[1][i], y_animation[1][i]), r, color="blue")
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.set_facecolor("forestgreen")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

# create empty lists for the x and y coordinates
x_animation, y_animation = ball_loc()
# create the figure and axes objects
fig, ax = plt.subplots()

# run the animation
ani = FuncAnimation(fig, animate, frames=len(x_animation[0]), interval=1, repeat=False)

plt.show()
