from requirements import *

class frame:
    def __init__(self, frame=None, base=np.zeros((6,1))):
        self.origin = base

        if frame is not None:
            self.origin = frame.origin + base

        print(self.origin)

    def T_mat(self, mechanism):
        return
    
class mechanism:
    def __init__(self, frame1, frame2):
        # The variables that would be referenced in a transformation matrix
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        self.ex = 0 # X-axis euler angle
        self.ey = 0 # Y-axis euler angle
        self.ez = 0 # Z-axis euler angle
        self.frame1 = frame1
        self.frame2 = frame2
 