"""
ROS 2 Onboard Node: Edge Anomaly Classifier & Closed-Loop ActuatorThis production-grade Python script implements a local ROS 2 node. It ingests high-frequency camera frames, simulates low-latency edge NPU inference, implements safety adjustments, and triggers predictive maintenance logging to a local JSON ledger.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
import json
import time

class AdvancedEdgePrinterController(Node):
    def __init__(self):
        super().__init__('advanced_edge_printer_controller')
        
        # 1. High-Frequency In-Situ Sensor Subscribers
        self.camera_sub = self.create_subscription(
            String, 
            '/sensor_optical_coherence_node', 
            self.analyze_meltpool_frame, 
            10
        )
        self.iot_sub = self.create_subscription(
            String, 
            '/sensor_iot_telemetry', 
            self.run_predictive_maintenance, 
            10
        )
        
        # 2. Real-Time Closed-Loop Control Actuator Publishers
        self.laser_pub = self.create_publisher(Float32, '/motor_actuator_driver_node/laser_power', 10)
        self.speed_pub = self.create_publisher(Float32, '/motor_actuator_driver_node/feed_rate', 10)
        
        # Local Diagnostics Ledger Target
        self.log_file_path = "local_predictive_maintenance_ledger.json"
        self.get_logger().info('Advanced Edge Node with Predictive Maintenance active.')

    def analyze_meltpool_frame(self, msg):
        """Simulates low-latency local NPU inference on an incoming meltpool frame."""
        try:
            frame_data = json.loads(msg.data)
            porosity_score = frame_data.get('porosity_index', 0.0)
            
            if porosity_score > 0.35:
                # Anomaly Detected: Trigger millisecond closed-loop correction
                self.execute_realtime_correction()
            else:
                self.maintain_baseline()
        except json.JSONDecodeError:
            self.get_logger().error('Malformed meltpool payload.')

    def execute_realtime_correction(self):
        """Publishes localized compensation commands within a 5ms window."""
        p_cmd = Float32()
        p_cmd.data = 280.0  # Boost power to melt un-fused powder clusters
        
        s_cmd = Float32()
        s_cmd.data = 950.0  # Slow down feed rate for deeper penetration
        
        self.laser_pub.publish(p_cmd)
        self.speed_pub.publish(s_cmd)

    def maintain_baseline(self):
        """Maintains nominal operating metrics under normal conditions."""
        p_cmd = Float32()
        p_cmd.data = 250.0  # Baseline power in Watts
        self.laser_pub.publish(p_cmd)

    def run_predictive_maintenance(self, msg):
        """Analyzes machine health signatures locally on the Edge NPU."""
        try:
            telemetry = json.loads(msg.data)
            vibration = telemetry.get('bearing_vibration_g', 1.2)
            temp = telemetry.get('galvo_mirror_temp_c', 42.0)
            
            # Diagnostic Anomaly Threshold Logic
            if vibration > 3.5 or temp > 75.0:
                self.get_logger().error('Predictive anomaly flagged! Committing to local ledger.')
                self.write_to_local_ledger(vibration, temp)
        except json.JSONDecodeError:
            self.get_logger().error('Failed to parse machine health data.')

    def write_to_local_ledger(self, vibration, temp):
        """Saves telemetry log locally, skipping costly cloud uploads."""
        log_entry = {
            "timestamp": time.time(),
            "status": "CRITICAL_MAINTENANCE_REQUIRED",
            "metrics": {"vibration_g": vibration, "mirror_temp_c": temp},
            "recommended_action": "Replace optic galvo assembly immediately."
        }
        with open(self.log_file_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

def main(args=None):
    rclpy.init(args=args)
    node = AdvancedEdgePrinterController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
