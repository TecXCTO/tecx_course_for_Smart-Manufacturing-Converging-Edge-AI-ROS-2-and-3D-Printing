#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32.hpp"
#include "qos_policy_config.hpp"

class LaserFeedbackNode : public rclcpp::Node {
public:
    LaserFeedbackNode() : Node("laser_feedback_node") {
        // Enforce the custom real-time QoS profile during publisher initialization
        laser_power_pub_ = this->create_publisher<std_msgs::msg::Float32>(
            "/motor_actuator_driver_node/laser_power", 
            industrial_am::qos::get_realtime_iot_profile()
        );
        
        RCLCPP_INFO(this->get_logger(), "Laser Feedback Node initialized with real-time QoS.");
    }

private:
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr laser_power_pub_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LaserFeedbackNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
