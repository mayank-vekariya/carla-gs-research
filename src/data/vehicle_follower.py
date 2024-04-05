# vehicle_follower.py
import carla
import time

def follow_vehicle(client, vehicle_id):
    """
    Follows the specified vehicle using the spectator view.
    """
    world = client.get_world()
    vehicle = world.get_actor(vehicle_id)
    spectator = world.get_spectator()

    while True:
        # Update the spectator's transform to follow the vehicle
        transform = vehicle.get_transform()
        spectator.set_transform(carla.Transform(transform.location + carla.Location(z=50), carla.Rotation(pitch=-90)))
        time.sleep(0.05)
