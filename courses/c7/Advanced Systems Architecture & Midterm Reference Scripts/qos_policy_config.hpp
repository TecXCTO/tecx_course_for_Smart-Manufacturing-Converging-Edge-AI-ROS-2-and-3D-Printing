// Real-Time QoS Configuration Template (C++)The following implementation builds a custom Quality of Service configuration profile using the native ROS 2 client library (rclcpp), optimizing communication pipelines for low latency.

#ifndef QOS_POLICY_CONFIG_HPP_
#define QOS_POLICY_CONFIG_HPP_

#include "rclcpp/rclcpp.hpp"

namespace industrial_am {
namespace qos {

inline rclcpp::QoS get_realtime_iot_profile() {
    // Instantiate a profile tracking only the most recent message frame
    rclcpp::QoS profile(rclcpp::KeepLast(1));

    // Best Effort avoids packet confirmation overhead to preserve low latency
    profile.best_effort();

    // Volatile durability drops historic message stores for late-joining nodes
    profile.durability_volatile();

    // Set a strict 10-millisecond deadline for real-time sensor delivery
    profile.deadline(rmw_time_t{0, 10000000}); // 10,000,000 nanoseconds

    return profile;
}

} // namespace qos
} // namespace industrial_am

#endif // QOS_POLICY_CONFIG_HPP_
