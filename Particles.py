from Vector import Vector

def BIB(R,lx=10,ly=10,lz=10):
    if  abs(R.x) > lx:
         R.x =  (R.x**2 - abs(R.x)*2*lx)/R.x
    if  abs(R.y) > ly:
         R.y =  (R.y**2 - abs(R.y)*2*ly)/R.y
    if  abs(R.z) > lz:
         R.z =  (R.z**2 - abs(R.z)*2*lz)/R.z
    return R

class Particle:
    
    '''
    Particles for the Simulator
    They hold kinematical variables: Position, Velocity and Acceleration
    And the trajectory of the particle, the time should be managed externally.
    
    '''
    
    # Syntax of Constructor 
    # Convention python "def" "any_name"(pass_the_name_of_obejct,maybe_some_args):
    def __init__(self,Name,Mass,Position,Velocity,Color):
        self.Nam = Name
        self.Mas = Mass
        self.Pos = Position
        self.Vel = Velocity
        self.Acc = Vector(0.,0.,0.)
        self.Col = Color
        self.TPos = []
        self.TVel = []
        self.TAcc = []

        self.IniPos = self.Pos
        self.IniVel = self.Vel
        self.IniAcc = self.Acc
    
    # One of the functions of the class
    def RemoveLastTrack(self):
        
        for i in range(3):
            del self.Tra[i][-1]

    def ClearTrajectory(self):
        self.TPos = []
        self.TVel = []
        self.TAcc = []
        self.Pos = self.IniPos
        self.Vel = self.IniVel
        self.Acc = self.IniAcc
        
    # Function that moves the particle in time according to its speed: 
    
    # self -> Actual Particle
    # dt   -> dt of the evolution
    
    # dPostion/dt = Velocity 
    # dVelocity/dt = Acceleration 
    
    
    def Evolve(self,dt,Omega=Vector(0.,0.,0.),Method="Euler"):
        
        if Method == "Euler":
            # dPosition = dt*Velocity
            self.Pos = self.Pos + self.Vel * dt
            
            # dVelocity = dt*Acceleration
            self.Vel = self.Vel + self.Acc * dt
        
        if Method == "Euler-Cromer":
            # dVelocity = dt*Acceleration
            self.Vel = self.Vel + self.Acc * dt
        
            # dPosition = dt*Velocity
            self.Pos = self.Pos + self.Vel * dt
        
        else: # Verlet 
            # Following: https://en.wikipedia.org/wiki/Verlet_integration
            # Section: Basic Störmer–Verlet
            if len(self.TPos) < 2:
                self.Pos += self.Vel * dt + 0.5*self.Acc*dt**2
            else:
                self.Pos = 2.0*self.TPos[-1] - self.TPos[-2] + self.Acc*dt**2
        
        # Record the Trajectory
        self.TPos.append(self.Pos)
        self.TVel.append(self.Vel)

class ChargedParticle(Particle):
    
    def __init__(self,Name,Mass,Charge,Position,Velocity,Color):
        super().__init__(Name,Mass,Position,Velocity,Color)
        self.charge = Charge
        
class periodic(Particle): 
    
    def Evolve(self,dt,Omega=Vector(0.,0.,0.),Method="Euler-Cromer"):
        
        if Method == "Euler":
            # dPosition = dt*Velocity
            self.Pos = self.Pos + self.Vel * dt
            
            # dVelocity = dt*Acceleration
            self.Vel = self.Vel + self.Acc * dt
        
        if Method == "Euler-Cromer":
            # dVelocity = dt*Acceleration
            self.Vel = self.Vel + self.Acc * dt
        
            # dPosition = dt*Velocity
            self.Pos = self.Pos + self.Vel * dt
        
        else: # Verlet 
            # Following: https://en.wikipedia.org/wiki/Verlet_integration
            # Section: Basic Störmer–Verlet
            
            LastAcc = (self.TAcc[-1]if len(self.TAcc)else Vector(0,0,0))
            
            self.Pos = self.Pos + self.Vel * dt + LastAcc *(0.5*dt**2)
            
            self.Vel = self.Vel + ( self.Acc + LastAcc) * (0.5*dt)
        
        self.Pos = BIB(self.Pos)
            
        # Record the Trajectory
        self.TPos.append(self.Pos)
        self.TVel.append(self.Vel)
        self.TAcc.append(self.Acc)
        

# Unmovable Particles
class Stationary(ChargedParticle):
    # These do not move
    def Evolve(self,dt,Omega=Vector(0.,0.,0.)):
        self.TPos.append(self.Pos)

# Charged Particle on a Torus
class PChargedParticle(ChargedParticle): 
    
    def Evolve(self,dt,Omega=Vector(0.,0.,0.)):
        
        # dVelocity = dt*Acceleration
        self.Vel = self.Vel + self.Acc * dt
        
        # dPosition = dt*Velocity
        self.Pos = self.Pos + self.Vel * dt 
        
        self.Pos = BIB(self.Pos)
            
        # Record the Trajectory
        self.TPos.append(self.Pos)
        self.TVel.append(self.Vel)