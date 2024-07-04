import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Robot Simulation')

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
class Robot:
    def __init__(self, x=0, y=0, speed=1, angle=0):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.fov_angle = 45 # field of view angle in degrees
        self.fov_length = 100 # field of view length
        

    def move(self):
        new_x = self.x + self.speed * math.cos(math.radians(self.angle))
        new_y = self.y + self.speed * math.sin(math.radians(self.angle))
        

        # Prevent system
        # Stop the robot from going out of the window
        if 0 <= new_x <= width:
            self.x = new_x
        if 0 <= new_y <= height:
            self.y = new_y
        

    def change_direction(self, angle):
        self.angle = angle

    def change_speed(self, speed):
        self.speed = speed

    def get_position(self):
        return (self.x, self.y)

    def get_direction_point(self, length=50):
        end_x = self.x + length * math.cos(math.radians(self.angle))
        end_y = self.y + length * math.sin(math.radians(self.angle))
        return (end_x, end_y)


    def detect_fire(self,fire_list):
        for fire in fire_list:
            fire_x, fire_y = fire
            distance = math.hypot(fire_x - self.x, fire_y - self.y)
            angle_to_fire = math.degrees(math.atan2(fire_y - self.y, fire_x - self.x))
            relative_angle = (self.angle - angle_to_fire + 360) % 360


            if distance <= self.fov_length and (relative_angle <= self.fov_angle / 2 or relative_angle >= 360 - self.fov_angle / 2):
                return True
        return False        

class UserInput:
    def __init__(self, robot):
        self.robot = robot

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.robot.change_speed(self.robot.speed + 1)
        if keys[pygame.K_DOWN]:
            self.robot.change_speed(self.robot.speed - 1)
        if keys[pygame.K_LEFT]:
            self.robot.change_direction(self.robot.angle - 5)
        if keys[pygame.K_RIGHT]:
            self.robot.change_direction(self.robot.angle + 5)

def draw_text(surface, text, position, font_size=30, color=BLACK):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def draw_fov(surface, robot, color):
    fov_points = []
    fov_points.append((robot.x,robot.y))
    for angle in range(-robot.fov_angle//2, robot.fov_angle//2 + 1, 5):
        end_x = robot.x + robot.fov_length * math.cos(math.radians(robot.angle + angle))
        end_y = robot.y + robot.fov_length * math.sin(math.radians(robot.angle + angle))
        fov_points.append((end_x,end_y))
    pygame.draw.polygon(surface, color, fov_points, 0)
    


    
# Simulation parameters
robot = Robot(x=width//2, y=height//2, speed=1, angle=0)
user_input = UserInput(robot)
running = True
clock = pygame.time.Clock()

# Example of fire locations
fires = [(200,200), (400,300), (600,450)]

# Simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    user_input.handle_input()

    # Move the robot
    robot.move()

    # Clear the screen
    window.fill(WHITE)

    # Draw the fires
    for fire in fires:
        pygame.draw.circle(window, RED, fire, 10)

    # Determine the FOV Color
    fov_color= GREEN if robot.detect_fire(fires) else BLUE

    # Draw the field of view
    draw_fov(window, robot, fov_color)
    
    # Draw the robot
    pygame.draw.circle(window, BLUE, (int(robot.x), int(robot.y)), 10)

    # Draw the laser indicating the direction
    direction_point = robot.get_direction_point()
    pygame.draw.line(window, RED, (int(robot.x), int(robot.y)), (int(direction_point[0]), int(direction_point[1])), 2)

    # Display the robot's coordinates
    coords = robot.get_position()
    draw_text(window, f'Coordinates: ({coords[0]:.2f}, {coords[1]:.2f})', (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
