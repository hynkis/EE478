#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped

current_pose = PoseStamped()

def pose_callback(msg):
    global current_pose
    current_pose = msg
    print("Pose Received")
    print("X : "+str(current_pose.pose.position.x)+", Y : "+str(current_pose.pose.position.y)+", Z : "+str(current_pose.pose.position.z))

if __name__ == "__main__":
    rospy.init_node("offb_node_py")

    state_sub = rospy.Subscriber("mavros/local_position/pose", PoseStamped, callback = pose_callback)
    local_vel_pub = rospy.Publisher("mavros/setpoint_velocity/cmd_vel", TwistStamped, queue_size=10)

    # Setpoint publishing MUST be faster than 2Hz
    rate = rospy.Rate(20)

    cmd_velocity = TwistStamped()
    cmd_velocity.twist.linear.x = 0
    cmd_velocity.twist.linear.y = 0
    cmd_velocity.twist.linear.z = 0

    # Send a few setpoints before starting
    for i in range(100):   
        if(rospy.is_shutdown()):
            break

        local_vel_pub.publish(cmd_velocity)
        rate.sleep()

    # main loop
    while(not rospy.is_shutdown()):
        ##################################################
        # PID Controller
        cmd_velocity.twist.linear.x = 0
        cmd_velocity.twist.linear.y = 0
        cmd_velocity.twist.linear.z = 0
        ##################################################

        local_vel_pub.publish(cmd_velocity)
        rate.sleep()
