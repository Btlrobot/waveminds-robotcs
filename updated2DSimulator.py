import tkinter as tk
from tkinter import ttk
import threading
import pygame
import math
import time
import random

class RobotControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot Control")

        # Speed control
        self.speed_label = ttk.Label(self, text="Speed:")
        self.speed_label.grid(column=0, row=0, padx=10, pady=10)
        self.speed = tk.DoubleVar(value=1.0)
        self.speed_entry = ttk.Entry(self, textvariable=self.speed)
        self.speed_entry.grid(column=1, row=0, padx=10, pady=10)

        # Direction control
        self.direction_label = ttk.Label(self, text="Direction (degrees):")
        self.direction_label.grid(column=0, row=1, padx=10, pady=10)
        self.direction = tk.DoubleVar(value=0.0)
        self.direction_entry = ttk.Entry(self, textvariable=self.direction)
        self.direction_entry.grid(column=1, row=1, padx=10, pady=10)

        # PID values display
        self.kp_label = ttk.Label(self, text="Kp:")
        self.kp_label.grid(column=0, row=2, padx=10, pady=10)
        self.kp_value = ttk.Label(self, text="0.5")
        self.kp_value.grid(column=1, row=2, padx=10, pady=10)

        self.ki_label = ttk.Label(self, text="Ki:")
        self.ki_label.grid(column=0, row=3, padx=10, pady=10)
        self.ki_value = ttk.Label(self, text="0.1")
        self.ki_value.grid(column=1, row=3, padx=10, pady=10)

        self.kd_label = ttk.Label(self, text="Kd:")
        self.kd_label.grid(column=0, row=4, padx=10, pady=10)
        self.kd_value = ttk.Label(self, text="0.05")
        self.kd_value.grid(column=1, row=4, padx=10, pady=10)

        # Fire information table
        self.tree = ttk.Treeview(self, columns=('Fire Number', 'Location', 'Size', 'Heat', 'On Fire'), show='headings')
        self.tree.heading('Fire Number', text='Fire Number')
        self.tree.heading('Location', text='Location')
        self.tree.heading('Size', text='Size')
        self.tree.heading('Heat', text='Heat')
        self.tree.heading('On Fire', text='On Fire')
        self.tree.grid(column=0, row=5, columnspan=3, padx=10, pady=10)

        # Control buttons
        self.start_button = ttk.Button(self, text="Start", command=self.start_simulation)
        self.start_button.grid(column=0, row=6, padx=10, pady=10)

        self.pause_button = ttk.Button(self, text="Pause", command=self.pause_simulation)
        self.pause_button.grid(column=1, row=6, padx=10, pady=10)

        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_simulation)
        self.reset_button.grid(column=2, row=6, padx=10, pady=10)

        # Pygame thread
        self.simulation_thread = None
        self.running = False

        # Shared speed and direction variables
        self.shared_speed = 10.0
        self.shared_direction = 0.0

        # PID controller parameters
        self.kp = 0.5
        self.ki = 0.1
        self.kd = 0.05
        self.pid_integral = 0
        self.pid_previous_error = 0
        self.pid_last_time = time.time()

        # Fire locations and info
        self.fires = [pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 20) for _ in range(3)]
        self.fires_info = [{'size': random.randint(1, 3), 'heat': random.randint(1, 3)} for _ in range(3)]

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.simulation_thread = threading.Thread(target=self.run_simulation)
            self.simulation_thread.start()

    def pause_simulation(self):
        self.running = False
        if self.simulation_thread:
            self.simulation_thread.join()

    def reset_simulation(self):
        self.running = False
        if self.simulation_thread:
            self.simulation_thread.join()
        global robot_pos, robot_angle, robot_speed
        robot_pos = [400, 300]
        robot_angle = 0
        self.shared_speed = 1.0
        self.shared_direction = 0.0
        self.speed.set(self.shared_speed)
        self.direction.set(self.shared_direction)
        self.pid_integral = 0
        self.pid_previous_error = 0
        self.fires = [pygame.Rect(random.randint(50, 750), random.randint(50, 550), 20, 20) for _ in range(3)]
        self.fires_info = [{'size': random.randint(1, 3), 'heat': random.randint(1, 3)} for _ in range(3)]
        self.tree.delete(*self.tree.get_children())

    def run_simulation(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Robot Simulation")
        global robot_pos, robot_angle

        clock = pygame.time.Clock()

        # Random buildings (rectangles) positions and sizes
        buildings = [pygame.Rect(random.randint(50, 650), random.randint(50, 450), random.randint(50, 100), random.randint(50, 100)) for _ in range(5)]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Autonomous movement
            robot_angle = self.shared_direction
            robot_speed = self.shared_speed
            radians = math.radians(robot_angle)
            new_x = robot_pos[0] + robot_speed * math.cos(radians)
            new_y = robot_pos[1] + robot_speed * math.sin(radians)

            # Check for border collisions and adjust direction
            if new_x < 10 or new_x > 790 or new_y < 10 or new_y > 590:
                self.shared_direction += random.randint(95, 160)  # Turn away from the border
                continue

            # Check for building collisions and adjust direction
            collision = False
            for building in buildings:
                if building.collidepoint(new_x, new_y):
                    self.shared_direction += 90  # Turn away from the building
                    collision = True
                    break

            if not collision:
                robot_pos[0] = new_x
                robot_pos[1] = new_y

            # Clear the screen
            screen.fill((255, 255, 255))

            # Draw the border
            pygame.draw.rect(screen, (0, 0, 0), (10, 10, 780, 580), 2)

            # Draw buildings and their perimeters
            for building in buildings:
                pygame.draw.rect(screen, (0, 0, 0), building, 0)
                pygame.draw.rect(screen, (0, 255, 0), building.inflate(20, 20), 2)

            # Draw the robot (a simple circle for this example)
            pygame.draw.circle(screen, (0, 0, 255), (int(robot_pos[0]), int(robot_pos[1])), 10)

            # Draw the direction line
            end_x = robot_pos[0] + 20 * math.cos(radians)
            end_y = robot_pos[1] + 20 * math.sin(radians)
            pygame.draw.line(screen, (255, 0, 0), (robot_pos[0], robot_pos[1]), (end_x, end_y), 2)

            # Draw the robot's field of view
            fov_radius = 100
            fov_angle = 45
            left_fov_x = robot_pos[0] + fov_radius * math.cos(math.radians(robot_angle - fov_angle / 2))
            left_fov_y = robot_pos[1] + fov_radius * math.sin(math.radians(robot_angle - fov_angle / 2))
            right_fov_x = robot_pos[0] + fov_radius * math.cos(math.radians(robot_angle + fov_angle / 2))
            right_fov_y = robot_pos[1] + fov_radius * math.sin(math.radians(robot_angle + fov_angle / 2))
            pygame.draw.polygon(screen, (0, 255, 255, 128), [(robot_pos[0], robot_pos[1]), (left_fov_x, left_fov_y), (right_fov_x, right_fov_y)], 1)

            # Display the robot's direction
            font = pygame.font.SysFont(None, 24)
            direction_text = font.render(f"Direction: {robot_angle:.2f} degrees", True, (0, 0, 0))
            screen.blit(direction_text, (10, 10))

            # Display the perimeter of a "house" (first building for this example)
            house = buildings[0]
            perimeter = 2 * (house.width + house.height)
            perimeter_text = font.render(f"House Perimeter: {perimeter} units", True, (0, 0, 0))
            screen.blit(perimeter_text, (10, 40))

            # Detect fires within the field of view
            for i, fire in enumerate(self.fires):
                fire_center = fire.center
                distance_to_fire = math.hypot(robot_pos[0] - fire_center[0], robot_pos[1] - fire_center[1])
                angle_to_fire = math.degrees(math.atan2(fire_center[1] - robot_pos[1], fire_center[0] - robot_pos[0])) - robot_angle

                if -fov_angle / 2 <= angle_to_fire <= fov_angle / 2 and distance_to_fire <= fov_radius:
                    # Update Tkinter table with fire information
                    location = f"({fire.x}, {fire.y})"
                    size = "Small" if self.fires_info[i]['size'] == 1 else "Medium" if self.fires_info[i]['size'] == 2 else "Large"
                    heat = "Low" if self.fires_info[i]['heat'] == 1 else "Medium" if self.fires_info[i]['heat'] == 2 else "High"
                    on_fire = any(building.collidepoint(fire_center[0], fire_center[1]) for building in buildings)
                    on_fire_text = "Yes" if on_fire else "No"

                    if len(self.tree.get_children()) <= i:
                        self.tree.insert('', 'end', values=(i + 1, location, size, heat, on_fire_text))
                    else:
                        self.tree.item(self.tree.get_children()[i], values=(i + 1, location, size, heat, on_fire_text))

                    # Draw perimeter around fire
                    pygame.draw.rect(screen, (255, 165, 0), fire.inflate(20, 20), 2)

                # Draw and animate fires
                pygame.draw.rect(screen, (255, 0, 0), fire, 0)
                # Simple fire animation effect (alternating size)
                fire.inflate_ip(random.randint(-1, 1), random.randint(-1, 1))

            # Update Tkinter speed value
            self.update_speed_direction()

            # Refresh the screen
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update_speed_direction(self):
        # Use the main thread to safely update the Tkinter variables
        self.speed.set(self.shared_speed)
        self.direction.set(self.shared_direction)
        self.kp_value.config(text=f"{self.kp:.2f}")
        self.ki_value.config(text=f"{self.ki:.2f}")
        self.kd_value.config(text=f"{self.kd:.2f}")

if __name__ == "__main__":
    robot_pos = [400, 300]
    robot_angle = 0  # in degrees
    robot_speed = 1.0  # units per frame

    app = RobotControlApp()
    app.mainloop()
