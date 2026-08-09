"""
C++ Reference: Measuring Real-Time Jitter & LatencyThis production-grade C++ node demonstrates how to calculate precise microsecond timing metrics. It measures processing latency and timing variation (jitter) for incoming high-speed edge telemetry packets.
"""
#include <chrono>
#include <memory>
#include <numeric>
#include <vector>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class LatencyJitterAnalyzerNode : public rclcpp::Node {
public:
    LatencyJitterAnalyzerNode() : Node("latency_jitter_analyzer_node") {
        // High-frequency telemetry ingestion subscription channel
        telemetry_sub_ = this->create_subscription<std_msgs::msg::String>(
            "/sensor_optical_coherence_node",
            10,
            std::bind(&LatencyJitterAnalyzerNode::telemetry_callback, this, std::placeholders::_1)
        );

        last_arrival_time_ = std::chrono::steady_clock::now();
        RCLCPP_INFO(this->get_logger(), "Real-Time Latency & Jitter Diagnostic Monitor Node Activated.");
    }

private:
    void telemetry_callback(const std_msgs::msg::String::SharedPtr msg) {
        auto current_time = std::chrono::steady_clock::now();
        
        // Calculate the exact elapsed duration since the previous message packet arrived
        auto delta_time = std::chrono::duration_cast<std::chrono::microseconds>(current_time - last_arrival_time_).count();
        last_arrival_time_ = current_time;

        // Skip calculations on the very first packet initialization run
        if (is_first_frame_) {
            is_first_frame_ = false;
            return;
        }

        latencies_us_.push_back(delta_time);

        // Keep rolling history bounds to the most recent 100 metric evaluations
        if (latencies_us_.size() > 100) {
            latencies_us_.erase(latencies_us_.begin());
        }

        compute_diagnostics_report();
    }

    void compute_diagnostics_report() {
        if (latencies_us_.size() < 2) return;

        double sum = std::accumulate(latencies_us_.begin(), latencies_us_.end(), 0.0);
        double mean_latency = sum / latencies_us_.size();

        // Compute Jitter (Standard Deviation of processing arrival offsets)
        double variance_accumulator = 0.0;
        for (const auto& latency : latencies_us_) {
            variance_accumulator += std::pow(latency - mean_latency, 2);
        }
        double jitter = std::sqrt(variance_accumulator / latencies_us_.size());

        // Emit structural logs to terminal window
        RCLCPP_INFO(this->get_logger(), "--- Real-Time System Profiler ---");
        RCLCPP_INFO(this->get_logger(), "Mean Arrival Latency: %.2f us", mean_latency);
        RCLCPP_INFO(this->get_logger(), "Calculated Deterministic Jitter: %.2f us", jitter);
        
        if (jitter > 500.0) { // Safety warning threshold if timing drifts by more than 0.5ms
            RCLCPP_WARN(this->get_logger(), "CRITICAL WARNING: Timing jitter exceeds real-time boundaries!");
        }
    }

    rclcpp::Subscription<std_msgs::msg::String::SharedPtr>::SharedPtr telemetry_sub_;
    std::chrono::steady_clock::time_point last_arrival_time_;
    std::vector<double> latencies_us_;
    bool is_first_frame_ = true;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LatencyJitterAnalyzerNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
