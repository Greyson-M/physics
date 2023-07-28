from slider import Slider

class GravSlider(Slider):
    def __init__(self, env, pos, size, initial_val, min, max) -> None:
        super().__init__(env, pos, size, initial_val, min, max)

    def action(self, val):
        self.environment.g = val