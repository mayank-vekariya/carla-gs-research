# camera_viewer.py
import carla
import cv2
import numpy as np
import tkinter as tk





def image_callback(image, camera_name, image_buffers):
    """
    Processes the image received from a camera and updates the corresponding buffer.
    """
    # Convert CARLA image to an OpenCV image
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))  # BGRA format
    array = array[:, :, :3]  # Drop the alpha channel
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Update the corresponding buffer
    image_buffers[camera_name] = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV


def display_camera_feeds(world, vehicle):
    bounding_box = vehicle.bounding_box
    vehicle_size = bounding_box.extent.x, bounding_box.extent.y, bounding_box.extent.z
    camera_positions = {
        'Front': carla.Transform(carla.Location(x=vehicle_size[0] * 1.5, z=vehicle_size[2])),
        'Back': carla.Transform(carla.Location(x=-vehicle_size[0] * 1.5, z=vehicle_size[2]), carla.Rotation(yaw=180)),
        'Front Left': carla.Transform(carla.Location(x=vehicle_size[0], y=-vehicle_size[1], z=vehicle_size[2]),
                                      carla.Rotation(yaw=45)),
        'Front Right': carla.Transform(carla.Location(x=vehicle_size[0], y=vehicle_size[1], z=vehicle_size[2]),
                                       carla.Rotation(yaw=-45)),
        'Back Left': carla.Transform(carla.Location(x=-vehicle_size[0], y=-vehicle_size[1], z=vehicle_size[2]),
                                     carla.Rotation(yaw=135)),
        'Back Right': carla.Transform(carla.Location(x=-vehicle_size[0], y=vehicle_size[1], z=vehicle_size[2]),
                                      carla.Rotation(yaw=-135)),
    }

    image_buffers = {}
    cameras = []
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    for camera_name, transform in camera_positions.items():
        camera = world.spawn_actor(camera_bp, transform, attach_to=vehicle)
        camera.listen(lambda image, name=camera_name: image_callback(image, name, image_buffers))
        cameras.append(camera)
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    try:
        while True:
            if image_buffers:
                # Resize images to fit 3 in a row according to the screen size
                resized_images = []
                for key, img in list(image_buffers.items()):
                    resized_image = cv2.resize(img, (screen_width // 3, screen_height // 2))
                    resized_images.append(resized_image)

                # Assuming you have 6 cameras, adjust if you have more or less
                top_row = np.hstack(resized_images[:3])
                bottom_row = np.hstack(resized_images[3:6])

                # Stack the two rows vertically to fit them into the screen
                combined_image = np.vstack((top_row, bottom_row))

                cv2.imshow('CARLA Cameras', combined_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        cv2.destroyAllWindows()
        for camera in cameras:
            camera.destroy()

    # Adjust 'screen_width' and 'screen_height' to your actual screen size
    display_camera_feeds(world, vehicle, screen_width, screen_height)
