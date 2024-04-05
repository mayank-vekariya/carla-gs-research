import carla
import os

class CameraManager:
    def __init__(self, world, vehicle):
        self.world = world
        self.vehicle = vehicle
        self.cameras = []

    def attach_cameras(self):
        bounding_box = self.vehicle.bounding_box
        vehicle_size = bounding_box.extent.x, bounding_box.extent.y, bounding_box.extent.z

        # Define camera attachment points and settings with descriptive names
        camera_positions = {
            'Front': carla.Transform(carla.Location(x=vehicle_size[0] * 1.5, z=vehicle_size[2])),
            'Back': carla.Transform(carla.Location(x=-vehicle_size[0] * 1.5, z=vehicle_size[2]), carla.Rotation(yaw=180)),
            'Front Left': carla.Transform(carla.Location(x=vehicle_size[0], y=-vehicle_size[1], z=vehicle_size[2]), carla.Rotation(yaw=45)),
            'Front Right': carla.Transform(carla.Location(x=vehicle_size[0], y=vehicle_size[1], z=vehicle_size[2]), carla.Rotation(yaw=-45)),
            'Back Left': carla.Transform(carla.Location(x=-vehicle_size[0], y=-vehicle_size[1], z=vehicle_size[2]), carla.Rotation(yaw=135)),
            'Back Right': carla.Transform(carla.Location(x=-vehicle_size[0], y=vehicle_size[1], z=vehicle_size[2]), carla.Rotation(yaw=-135)),
        }

        camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        camera_bp.set_attribute('fov', '110')

        # Attach cameras and assign names based on positions
        for position, transform in camera_positions.items():
            camera = self.world.spawn_actor(camera_bp, transform, attach_to=self.vehicle)
            camera.listen(lambda image, name=position: self.save_image(image, name))
            self.cameras.append((camera, position))  # Store tuple of camera and position

    def save_image(self, image, camera_name):
        image_folder = f"./output/{camera_name}"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        image.save_to_disk(os.path.join(image_folder, f"{image.frame}.png"))

    def destroy_cameras(self):
        for camera, _ in self.cameras:
            camera.stop()
            camera.destroy()
        self.cameras = []
