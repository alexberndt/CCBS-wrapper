class PlanItem(object):
    def __init__(self, robot_id, t_s, start, t_g, goal, yaw=0):
        self.robot_id   = robot_id
        self.t_s        = t_s 
        self.start      = start     # {"x": 8, "y": 9}
        self.t_g        = t_g
        self.goal       = goal      # {"x": 8, "y": 9}

    def get_info(self):
        info = "\t--------------- \n"
        info += "\tt_s: {} \n".format(self.t_s)
        info += "\tstart: {} \n".format(self.start)
        info += "\tt_g: {} \n".format(self.t_g)
        info += "\tgoal: {} \n".format(self.goal)
        info += "\t---------------"
        return info