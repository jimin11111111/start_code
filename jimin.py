import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rclpy.parameter import Parameter
import math
from mechaship_interfaces.msg import ClassificationArray, DetectionArray
from mechaship_interfaces.srv import Key, ThrottlePercentage, RGBColor, ThrottlePulseWidth
import datetime
import time

class jimin(Node):
    def __init__(self):
        super().__init__(
            "jimin_node",
            allow_undeclared_parameters=True,
            automatically_declare_parameters_from_overrides=True,
        )
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=3,
        )
        self.set_key_handler = self.create_client(Key, "/actuators/key/set")
        self.set_throttle_handler = self.create_client(
            ThrottlePercentage, "/actuators/throttle/set_percentage"
        )
        self.set_throttle_handler_pulse = self.create_client(
            ThrottlePulseWidth, "/actuators/throttle/set_pulse_width"
        )

        self.run()
        print("end")

    def run(self):
        key = Key.Request()
        throttle = ThrottlePercentage.Request()

        print("1")
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).total_seconds() < 5:
            throttle = ThrottlePercentage.Request()
            throttle.percentage = 50
            print("tlqkf")
            self.set_throttle_handler.call_async(throttle)
            time.sleep(1)
        while 5 <(datetime.datetime.now() - start_time).total_seconds() < 10:
            key = Key.Request()
            key.degree = 60
            throttle1 = ThrottlePulseWidth.Request()
            throttle1._pulse_width = 1300
            self.set_key_handler.call_async(key)
            self.set_throttle_handler_pulse.call_async(throttle1)
            time.sleep(1)
            print("끝")
        throttle.percentage = 0
        key.degree = 90
        print("찐막")
        self.set_throttle_handler.call_async(throttle)
        self.set_key_handler.call_async(key)

        
def main(args=None):
    rclpy.init(args=args)
    node = jimin()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)")

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
