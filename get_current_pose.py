#include <ros/ros.h>
#include <franka_hw/franka_pose_cartesian_interface.h>
#include <geometry_msgs/Pose.h>

int main(int argc, char** argv) {
    ros::init(argc, argv, "get_pose_example");
    ros::NodeHandle nh;
    ros::Rate loop_rate(10);

    // franka_hw interfaces initialization
    franka_hw::FrankaPoseCartesianInterface* pci;
    try {
        pci = nh.get<franka_hw::FrankaPoseCartesianInterface>("<arm_id>_robot");
        ROS_INFO("Successfully connected to the robot interface.");
    } catch(const hardware_interface::HardwareInterfaceException& e) {
        ROS_ERROR_STREAM("Error connecting to FrankaPoseCartesianInterface: " << e.what());
        return 1;
    }

    while (ros::ok()) {
        // Reading the current robot state
        geometry_msgs::Pose current_pose = pci->getRobotPose();
        ROS_INFO_STREAM("Current Robot Pose: \n" << "Position - x: " << current_pose.position.x 
                                                 << ", y: " << current_pose.position.y
                                                 << ", z: " << current_pose.position.z
                                                 << "\nOrientation - x: " << current_pose.orientation.x
                                                 << ", y: " << current_pose.orientation.y
                                                 << ", z: " << current_pose.orientation.z
                                                 << ", w: " << current_pose.orientation.w);
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}
