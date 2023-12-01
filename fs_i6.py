import rclpy
from rclpy.node import Node
from dynamixel_controller_pkg.msg import MotorSpeeds
import serial
from threading import Thread

class RemoteControl(Node):
    def __init__(self):
        super().__init__('remote_control')
        self.publisher = self.create_publisher(MotorSpeeds, '/dual_motor_speed', 10)
        self.ser = serial.Serial('/dev/ttyUSB1', 115200)  # 調整為您的設定
        self.remote_thread = Thread(target=self.read_remote)
        self.remote_thread.start()

    def read_remote(self):
        R_speed = 0  # 初始化R_speed
        L_speed = 0  # 初始化L_speed
        while rclpy.ok():
            if self.ser.in_waiting:
                self.data_raw = self.ser.readline()  # 讀取一行
                self.data = self.data_raw.decode()   # 用預設的UTF-8解碼
                # 解析接收到的数据，确保为有效数据
                if self.data[-3:-2] == 'R':
                    R_speed = int(self.data[:-3])
                else:
                    L_speed = int(self.data[:-3])
                msg = MotorSpeeds()
                msg.motor_speed1 = R_speed
                msg.motor_speed2 = L_speed
                self.publisher.publish(msg)
                print(L_speed, R_speed)


def main(args=None):
    rclpy.init(args=args)
    remote_control = RemoteControl()
    rclpy.spin(remote_control)
    remote_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
