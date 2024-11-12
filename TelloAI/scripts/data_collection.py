import csv
from djitellopy import Tello
import time
import keyboard  # 用于非阻塞键盘输入

# 初始化无人机
tello = Tello()
tello.connect()
tello.streamon()
print("Battery level:", tello.get_battery())

# 创建CSV文件记录控制指令
csv_file_path = "C:/TelloMazeNavigation/data/flight_data.csv"
csv_file = open(csv_file_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["frame_count", "control"])  # 使用帧计数作为标识

try:
    tello.takeoff()
    time.sleep(1)

    # 初始化帧计数、时间戳和动作标志
    frame_count = 0
    last_action_time = time.time()
    action_executed = False  # 动作是否在当前秒内执行

    while True:
        # 当前时间
        current_time = time.time()

        # 如果时间超过一秒，重置动作标志和时间戳
        if current_time - last_action_time >= 1:
            last_action_time = current_time
            action_executed = False  # 允许在新的一秒内执行动作

        # 如果还没有在当前秒内执行动作，则检查键盘输入
        if not action_executed:
            # 非阻塞键盘输入控制
            if keyboard.is_pressed("w"):
                print("按下 'w' 键，前进")
                tello.move_forward(25)
                csv_writer.writerow([frame_count, "forward"])
                action_executed = True
                time.sleep(1)  # 增加1秒延迟

            elif keyboard.is_pressed("s"):
                print("按下 's' 键，后退")
                tello.move_back(25)
                csv_writer.writerow([frame_count, "backward"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("a"):
                print("按下 'a' 键，左移")
                tello.move_left(25)
                csv_writer.writerow([frame_count, "left"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("d"):
                print("按下 'd' 键，右移")
                tello.move_right(25)
                csv_writer.writerow([frame_count, "right"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("r"):
                print("按下 'r' 键，上升")
                tello.move_up(20)
                csv_writer.writerow([frame_count, "up"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("f"):
                print("按下 'f' 键，下降")
                tello.move_down(20)
                csv_writer.writerow([frame_count, "down"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("e"):
                print("按下 'e' 键，顺时针旋转")
                tello.rotate_clockwise(15)
                csv_writer.writerow([frame_count, "rotate_clockwise"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("q"):
                print("按下 'q' 键，逆时针旋转")
                tello.rotate_counter_clockwise(15)
                csv_writer.writerow([frame_count, "rotate_counter_clockwise"])
                action_executed = True
                time.sleep(1)

            elif keyboard.is_pressed("x"):
                print("降落...")
                tello.land()
                break

            # 增加帧计数
            frame_count += 1

except Exception as e:
    print("发生错误:", e)

finally:
    # 释放资源
    csv_file.close()
    tello.end()


