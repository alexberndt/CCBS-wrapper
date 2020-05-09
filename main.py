from ccbs_planner import CCBS_Planner
from planitem import PlanItem

def main():
    ccbs_planner    = CCBS_Planner("map.xml", [])
    global_map      = ccbs_planner.get_map()
    goal_locations  = ccbs_planner.get_goal_locations()

    # From the available goal locations, 
    # define a task for each AGV
    task_defintion  = {0: {"start": 1, "goal": 3}, 
                       1: {"start": 2, "goal": 5}}

    # run the global plan
    global_plan     = ccbs_planner.solve(task_defintion)

    print("Global plan")
    for robot_id in global_plan:
        print("-----------------------------")
        print("Robot ID: {}".format(robot_id))
        for planitem in global_plan[robot_id]:
            print(planitem.get_info())

    # set a new task definition
    task_defintion  = {0: {"start": 5,  "goal": 1}, 
                       1: {"start": 15, "goal": 2}}

    # run the global plan again
    global_plan     = ccbs_planner.solve(task_defintion)

    print("Global plan")
    for robot_id in global_plan:
        print("-----------------------------")
        print("Robot ID: {}".format(robot_id))
        for planitem in global_plan[robot_id]:
            print(planitem.get_info())

if __name__ == "__main__":
    main()