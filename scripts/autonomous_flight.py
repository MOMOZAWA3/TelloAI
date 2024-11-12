import csv
from djitellopy import Tello
import time

# 初始化 Tello 无人机
tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()

# 读取 CSV 文件中的指令数据
csv_file_path = "C:/TelloMazeNavigation/data/flight_data.csv"
with open(csv_file_path, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # 跳过标题行

    try:
        for row in csv_reader:
            frame_count, action = row

            # 根据动作指令执行控制
            if action == "forward":
                tello.move_forward(20)
            elif action == "backward":
                tello.move_back(20)
            elif action == "left":
                tello.move_left(20)
            elif action == "right":
                tello.move_right(20)
            elif action == "rotate_clockwise":
                tello.rotate_clockwise(15)
            elif action == "rotate_counter_clockwise":
                tello.rotate_counter_clockwise(15)
            elif action == "up":
                tello.move_up(20)
            elif action == "down":
                tello.move_down(20)

            # 短暂延时，确保每个动作完成
            time.sleep(0.1)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        tello.land()
        tello.end()
