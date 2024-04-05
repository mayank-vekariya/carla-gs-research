import carla

class SimulationManager:
    def __init__(self, world):
        self.world = world

    def set_weather(self, weather_type):
        weather = getattr(carla.WeatherParameters, weather_type, None)
        if weather:
            self.world.set_weather(weather)
