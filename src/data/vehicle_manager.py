import carla
import random

class VehicleManager:
    def __init__(self, world):
        self.world = world
        self.vehicle = None

    def spawn_vehicle(self, auto_pilot=False, vehicle_type='model3'):
        blueprint_library = self.world.get_blueprint_library()
        vehicle_bp = random.choice(blueprint_library.filter(vehicle_type))
        spawn_point = random.choice(self.world.get_map().get_spawn_points())
        self.vehicle = self.world.spawn_actor(vehicle_bp, spawn_point)
        self.vehicle.set_autopilot(auto_pilot)
        return self.vehicle

    def destroy_vehicle(self):
        if self.vehicle:
            self.vehicle.destroy()
