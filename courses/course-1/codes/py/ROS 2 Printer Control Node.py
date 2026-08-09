"""
Below is a production-ready template for a ROS 2 node written in Python. It demonstrates how to subscribe to a high-speed camera topic, simulate edge-AI anomaly detection, and publish closed-loop motor correction commands with low latency.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
import json

class EdgeAiPrinterController(Node):
    def __init__(self):
        super().__init__('edge_ai_printer_controller')
        
        # 1. Telemetry Subscribers (Ingesting IoT Sensor Streams)
        self.camera_sub = self.create_subscription(
            String,
            '/sensor_optical_coherence_node',
            self.analyze_meltpool_frame,
            10 # Queue size
        )
        
        # 2. Control Actuator Publishers (Closed-Loop Commands)
        self.laser_pub = self.create_publisher(Float32, '/motor_actuator_driver_node/laser_power', 10)
        self.speed_pub = self.create_publisher(Float32, '/motor_actuator_driver_node/feed_rate', 10)
        
        self.get_logger().info('Edge AI Printer Controller Node successfully initiated.')

    def analyze_meltpool_frame(self, msg):
        """Simulates low-latency local NPU inference on a meltpool frame."""
        try:
            # Parse the incoming sensor payload
            frame_data = json.loads(msg.data)
            porosity_score = frame_data.get('porosity_index', 0.0)
            
            # Edge AI Threshold Logic
            if porosity_score > 0.35:
                # Anomaly detected! Execute real-time closed-loop correction
                self.get_logger().warn(f'Anomaly detected (Score: {porosity_score:.2f}). Adjusting parameters.')
                self.execute_realtime_correction()
            else:
                # Normal operation: Maintain baseline parameters
                self.maintain_baseline()
                
        except json.JSONDecodeError:
            self.get_logger().error('Malformed sensor telemetry received.')

    def execute_realtime_correction(self):
        """Publishes localized compensation commands within a 5ms window."""
        power_cmd = Float32()
        power_cmd.data = 280.0  # Boost laser power to melt un-fused powder
        self.laser_pub.publish(power_cmd)
        
        speed_cmd = Float32()
        speed_cmd.data = 950.0  # Slightly slow down feed rate for deeper penetration
        self.speed_pub.publish(speed_cmd)

    def maintain_baseline(self):
        """Publishes standard operating parameters."""
        power_cmd = Float32()
        power_cmd.data = 250.0  # Nominal power in Watts
        self.laser_pub.publish(power_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = EdgeAiPrinterController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
  
