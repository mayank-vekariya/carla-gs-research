import carla
import argparse
from vehicle_manager import VehicleManager
from camera_manager import CameraManager
from simulation_manager import SimulationManager
from traffic_manager import TrafficManager
from environment_manager import EnvironmentManager
from vehicle_follower import follow_vehicle
from camera_viewer import display_camera_feeds
import threading

def main():
    # Initialize the client
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    # Get the world
    world = client.get_world()

    # Initialize Managers
    simulation_manager = SimulationManager(world)
    environment_manager = EnvironmentManager(world)
    vehicle_manager = VehicleManager(world)
    # traffic_manager = TrafficManager(world, client.get_trafficmanager())

    try:
        # simulation_manager.set_weather(args.weather)
        # environment_manager.load_scenario(args.scenario)
        vehicle = next(filter(lambda x: x.type_id.startswith('vehicle.'), world.get_actors()), None)
        if vehicle is None:
            print("Vehicle not found. Make sure the vehicle is spawned.")
            return

        # Start camera feeds in a separate thread
        camera_thread = threading.Thread(target=display_camera_feeds, args=(world, vehicle), daemon=True)
        camera_thread.start()

        # Start vehicle follower in a separate
        follow_thread = threading.Thread(target=follow_vehicle, args=(client, vehicle.id), daemon=True)
        follow_thread.start()

        # camera_manager = CameraManager(world, vehicle)
        # camera_manager.attach_cameras()
        # traffic_manager.configure_traffic(density=args.traffic_density)

        print("Starting data collection...")
        while True:
            pass  # Data collection or waiting for an exit condition

    except KeyboardInterrupt:
        print("\nCancelled by user. Cleaning up...")
    finally:
        print("Destroying actors...")
        # camera_manager.destroy_cameras()
        vehicle_manager.destroy_vehicle()
        print("Data collection stopped.")


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='CARLA Data Collection')
    # parser.add_argument('--host', type=str, default='localhost', help='CARLA host')
    # parser.add_argument('--port', type=int, default=2000, help='CARLA port')
    # parser.add_argument('--weather', type=str, default='Clear', help='Weather condition')
    # parser.add_argument('--scenario', type=str, default='Town01', help='Simulation scenario/map')
    # parser.add_argument('--vehicle_type', type=str, default='model3', help='Type of vehicle to spawn')
    # parser.add_argument('--autopilot', action='store_true', help='Enable autopilot')
    # parser.add_argument('--traffic_density', type=float, default=0.5, help='Traffic density (0.0 to 1.0)')
    # args = parser.parse_args()

    main()
