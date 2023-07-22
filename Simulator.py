import matplotlib.pyplot as plt
from tqdm import tqdm
from Vector import Vector

class Simulator:
    
    '''
    
    Deals with Time management and Interactions
    Democratic treatment of all particles

    
    '''
    def __init__(self,**kwargs):
        self.Velocity    = Vector(0,0,0)
        self.Omega       = Vector(0,0,0)
        self.Particles   = kwargs["Particles"]
        self.Interaction = kwargs["Interaction"]
        self.External    = kwargs["External"]
        self.Time        = []
        
    def Simulate(self,Time,Steps):
        
        # Simulation Environment 
        # Computes force on all particles
        
        t = 0
        dt = Time/Steps
        for _ in tqdm(range(Steps)):
        
        #while t < Time:
            #print("Working on:",t)
            #t += dt
            
            # Compute the forces on each particle and modify the 
            # particle's acceleration accordingly
            for i, Particle1 in enumerate(self.Particles):
                # Compute the total force on particle i
                Acc = self.External(Particle1)
                for j, Particle2 in enumerate(self.Particles):
                    # Compute the contribution to the force on particle i from particle j
                    # Skip slef interactions
                    if i == j: 
                        continue
                    # Compute force and acceleration & set the accelerations
                    Acc = Acc + self.Interaction(Particle1,Particle2)
                Particle1.Acc = (1.0/Particle1.Mas)*Acc
            # Time Evolution, this is handled by particles themselves
            for Particle in self.Particles:
                Particle.Evolve(dt,self.Omega)
        
    def GeneratePlots(self,mode="Show"):
        
        plt.clf()
        plt.title("Trajectories")
        for Particle in self.Particles:
            x = [ P.x for P in Particle.TPos ]
            y = [ P.y for P in Particle.TPos ]
            plt.plot(x,y,label=Particle.Nam)
        plt.legend(loc="best")
        if(mode=="Show"):
            plt.show()
        elif (mode=="Save"):
            plt.savefig("Trajectories.png")

    def ClearTrajectories(self):
        for Particle in self.Particles:
            Particle.ClearTrajectory()