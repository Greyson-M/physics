import numpy as np

class System():
    def __init__(self, env, masses, constraints) -> None:
        self.masses = masses
        self.constraints = constraints
        self.env = env
        self.camera = self.env.camera

        self.mass = 0
        self.mass_center = np.array((0, 0))
        self.base_mass = None
        self.control_mass = None
        self.mass_count = len(self.masses)

        for mass in self.masses:
            self.mass += mass.mass

            if mass.name == "Base":
                self.base_mass = mass
            elif mass.name == "Control":
                self.control_mass = mass

        if self.base_mass == None:
            raise Exception("No Base Mass")
        if self.control_mass == None:
            raise Exception("No Control Mass")

        for mass in self.masses:
            self.mass_center[0] += mass.pos[0] * mass.mass
            self.mass_center[0] /= self.mass
            self.mass_center[1] += mass.pos[1] * mass.mass
            self.mass_center[1] /= self.mass

        self.p2 = self.base_mass
        self.p1 = self.control_mass

    def applyForce(self, force):
        for mass in self.masses:
            mass.applyForce(force/self.mass_count)

    def applyControl(self, force):
        self.control_mass.applyForce(force)

    def get_angle(self):
        dx = self.p2.pos[0] - self.p1.pos[0]
        dy = self.p2.pos[1] - self.p1.pos[1]

        angle = np.arctan2(dy, dx)

        return angle


        


    
        
        

    