

import os
import subprocess
import xml.etree.cElementTree as ET
from xml.dom import minidom

class PlanItem(object):
    def __init__(self, robot_id, t, x, y, vertex, yaw=0):
        self.robot_id   = robot_id
        self.t          = time 
        self.x          = x
        self.y          = y 
        self.yaw        = yaw 
        self.vertex     = vertex

class GlobalPlan(object):
    def __init__(self, map_file, goal_locations):
        self.map_file   = map_file # local reference to a map file
        self.pwd = os.path.dirname(os.path.realpath(__file__))

        # DEFINE FILE LOCATIONS
        self.map_dir    = self.pwd + "/maps/"
        self.task_dir   = self.pwd + "/tasks/"
        self.ccbs_dir   = self.pwd + "/CCBS_graphs/"

        self.goal_locations = goal_locations # List of goal locations

        self.task_cnt   = 0

    def run_task(self, task_description):
        
        # task_description
        # Dictionary of AGVs with start and goal positions { 0: {"start": 1, "goal": 3}, 1: {"start": 2, "goal": 5} }
        
        self.task_file       = self._create_task_file(task_description) 
        self.task_log_file   = self.task_file.split(".")[0] + "_log." + self.task_file.split(".")[1]

        # RUN THE CCBS ALGORITHM
        try:
            subprocess.run(
                [self.ccbs_dir + "C-CBS",
                self.map_dir  + self.map_file,
                self.task_dir + self.task_file
                ],
                check=True)
        except:
            pass
 
        # READ THE TASK_LOG FILE
        return self.task_log_file

    def get_map(self):
        print("get_map called!")

    def get_goal_locations(self):
        print("get_goal_locations called!")

    def _create_task_file(self, task_description):
        print("_create_task_file")

        self.task_cnt += 1
        task_file_name = "task_" + str(self.task_cnt) + ".xml"

        et = ET.parse(self.task_dir + "task_empty.xml")
        
        for agent_id in task_description:
            start_node  = task_description[agent_id]["start"]
            goal_node   = task_description[agent_id]["goal"]

            agent = ET.SubElement(et.getroot(), "agent")
            agent.attrib["start_id"]    = str(start_node)
            agent.attrib["goal_id"]     = str(goal_node)

        xml_string = (minidom.parseString(ET.tostring(et.getroot())).toprettyxml(indent=" "))

        root    = ET.fromstring(xml_string)
        tree    = ET.ElementTree(root)
        tree.write(open(self.task_dir + task_file_name, "wb")) #, encoding="UTF-8")

        return task_file_name

    def _get_map_details(self):
        print("_get_map_details")

if __name__ == "__main__":

    global_plan     = GlobalPlan("map.xml", [])
    global_map      = global_plan.get_map()
    goal_locations  = global_plan.get_goal_locations()

    # From the available goal locations, 
    # define a task for each AGV
    
    task_defintion  = {0: {"start": 1, "goal": 3}, 
                       1: {"start": 2, "goal": 5}}

    # run the global plan
    global_plan.run_task(task_defintion)

    # set a new task definition
    task_defintion  = {0: {"start": 5,  "goal": 1}, 
                       1: {"start": 15, "goal": 2}}

    # run the global plan again
    global_plan.run_task(task_defintion)