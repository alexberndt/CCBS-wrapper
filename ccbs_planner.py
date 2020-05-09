import os
import subprocess
import xml.etree.cElementTree as ET
from xml.dom import minidom
import xmltodict
from planitem import PlanItem

class CCBS_Planner(object):
    def __init__(self, map_file, goal_locations):
        self.map_file   = map_file # local reference to a map file
        self.pwd = os.path.dirname(os.path.realpath(__file__))

        # DEFINE FILE LOCATIONS
        self.map_dir    = self.pwd + "/maps/"
        self.task_dir   = self.pwd + "/tasks/"
        self.ccbs_dir   = self.pwd + "/CCBS/"

        self.goal_locations = goal_locations # List of goal locations

        self.task_cnt   = 0

    def solve(self, task_description):
        
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

        global_plan = {}
 
        # READ THE TASK_LOG FILE
        print("opening task log file: {}".format(self.task_log_file))

        with open(self.task_dir + self.task_log_file) as fd:
            task_log = xmltodict.parse(fd.read())
        # 1) Create vertices and Type 1 dependencies
        for agent in task_log["root"]["log"]["agent"]:
            _id = int(agent["@number"])
            _plan = agent["path"]["hplevel"]["section"]
            
            global_plan[_id] = []

            cumulative_length = 0.0
            for action in _plan:

                start   = {"x": float(action["@start.x"]), "y": float(action["@start.y"])}
                goal    = {"x": float(action["@finish.x"]),"y": float(action["@finish.y"])}
                length  = float(action["@length"]) # length = time to stay here
                t_s     = cumulative_length
                cumulative_length += length
                t_g     = cumulative_length

                # Only add if no start/goal
                if not (start == goal and t_s == t_g):
                    plan_item = PlanItem(_id, t_s, start, t_g, goal)
                    global_plan[_id].append(plan_item)
            
            # self.vertices[_id] = []
            # cumulative_length = 0
            # v_no = 0    # vertex number
            # _prev_vertex = None
            # for action in _plan:
            #     # extract data
            #     start   = {"x": float(action["@start.x"]), "y": float(action["@start.y"])}
            #     goal    = {"x": float(action["@finish.x"]),"y": float(action["@finish.y"])}
            #     length  = float(action["@length"]) # length = time to stay here
            #     t_s     = cumulative_length
            #     cumulative_length += length
            #     t_g     = cumulative_length
            #     # if start and finish are the same, do not create ADG vertex
            #     eps = 0.001
            #     if (abs(start["x"] - goal["x"]) < eps and abs(start["y"] - goal["y"]) < eps):
            #         # do not create new vertex
            #         continue
            #     # create new vertex
            #     _vertex = Vertex(_id, v_no, t_s, t_g, start, goal, Status.STAGED)
            #     v_no += 1
            #     self.vertices[_id].append(_vertex)
            #     # Add Type 1 dependencies
            #     if _prev_vertex is not None:
            #         self._add_edge(_prev_vertex, _vertex)
            #     _prev_vertex = _vertex
            
            # init AGVs
            # self.AGVs[_id] = Agv(_id, self.vertices[_id])
            # self.AGVcnt += 1

        return global_plan

    def get_map(self):
        print("get_map called!")

    def get_goal_locations(self):
        print("get_goal_locations called!")

    def _create_task_file(self, task_description):
        print("_create_task_file")

        self.task_cnt += 1
        task_file_name = "task_" + str(self.task_cnt) + ".xml"
        print("task_file_name: {}".format(task_file_name))

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