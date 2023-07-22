import numpy as np
from Vector import Vector

class Camera:
    def __init__(self,**kwargs):
        pars = {"Distance":1,"Orientation":Vector(0,0,-1),"Position":Vector(0,0,10)}
        pars.update(**kwargs)
        self.Orientation = pars["Orientation"] # Vector Normal to the plane
        self.Position    = pars["Position"]    # Location of the camera
        self.Distance    = pars["Distance"]    # Distance from the camera to the screeen (in the direction of "Orientation")
        
        r_trans          = np.sqrt(self.Orientation.x**2+self.Orientation.y**2)
        
        # Local Coordinates on the plane
        self.u_theta     = Vector(-self.Orientation.y/r_trans,self.Orientation.x/r_trans,0)
        self.u_phi       = Vector(self.Orientation.x*self.Orientation.z/r_trans,
                                  self.Orientation.y*self.Orientation.z/r_trans,
                                  -r_trans)
    def Convert(self,Position):
        r     = Position - self.Position
        Proj  = self.Orientation*r
        rscal = ( r * (self.Distance/Proj) if Proj > 0 else Vector(0,0,0) )
        return Vector(self.u_theta*rscal,self.u_phi*rscal,0)