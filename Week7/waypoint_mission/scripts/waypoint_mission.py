#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyResponse
from geometry_msgs.msg import Point

# Waypoints [[X list], [Y list], [Z list]]
waypoint_list = [[1, 2, 3], \
                [1, 2, 3], \
                [1, 2, 3]]

class WaypointMission:
    def __init__(self):
        self.cur_waypoint_idx = -1
        self.cur_waypoint = Point()

        self.waypoint_server = rospy.Service("request_next_waypoint", Empty, self.waypoint_service)
        self.waypoint_pub = rospy.Publisher("waypoint_manager_target", Point, queue_size = 10)
        # self.cur_position_sub = rospy.Subscriber("cur_position", , self.auto_arrive_checker_cb, queue_size=1)

        rospy.loginfo("Waypoint mission manager is now avilable!")

        # Initialize target waypoint to first waypoint
        self.get_next_waypoint()

    def waypoint_service(self, req):
        if(self.get_next_waypoint()):
            rospy.loginfo("Waypoint updated")
        else:
            rospy.logerr("Waypoint update failed")
        return EmptyResponse()
    
    def get_next_waypoint(self):
        if(self.cur_waypoint_idx < len(waypoint_list[0]) - 1):
            self.cur_waypoint_idx = self.cur_waypoint_idx + 1

        else:
            print("All waypoint mission are already been finished")
            return False
        
        self.cur_waypoint.x = waypoint_list[0][self.cur_waypoint_idx]
        self.cur_waypoint.y = waypoint_list[1][self.cur_waypoint_idx]
        self.cur_waypoint.z = waypoint_list[2][self.cur_waypoint_idx]

        return True
    
    # def auto_arrive_checker_cb():
        # dist calc_dist(cur_waypoint, cur_drone_pose)
        # if(dist < threshold)
        #   get_next_waypoint()
        # TODO Optionally
        
    def run(self):
        self.waypoint_pub.publish(self.cur_waypoint)
    
    def check_waypoint_list(self):
        for dim in range(0, len(waypoint_list) - 2):
            if (len(waypoint_list[dim]) != len(waypoint_list[dim+1])):
                return False
            
        return True
    
if __name__ == '__main__':
    rospy.init_node("waypoint_mission_node")
    rate = rospy.Rate(10)

    wp_mission = WaypointMission()
    if not wp_mission.check_waypoint_list():
        rospy.logerr("Waypoint is not well formed")
        quit()

    while not rospy.is_shutdown():
        wp_mission.run()
        rate.sleep()


