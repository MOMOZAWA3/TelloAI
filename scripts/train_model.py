import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2
import pandas as pd

# 加载和预处理视频数据
def load_data_from_video(video_path, csv_file):
    data = pd.read_csv(csv_file)
    video = cv2.VideoCapture(video_path)
    images = []
    labels = []

    # 视频帧率
    fps = video.get(cv2.CAP_PROP_FPS)

    # 遍历 CSV 文件，逐帧处理视频
    for index, row in data.iterrows():
        frame_count = row["frame_count"]  # 使用 frame_count 代替 timestamp
        control = row["control"]

        # 设置帧数并读取该帧
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, frame = video.read()
        if not ret:
            print(f"帧读取失败: 帧数 {frame_count}")
            continue

        # 调整图像大小并正则化
        frame = cv2.resize(frame, (128, 128)) / 255.0
        images.append(frame)

        # 将控制指令转为标签
        if control == "forward":
            labels.append(0)
        elif control == "backward":
            labels.append(1)
        elif control == "left":
            labels.append(2)
        elif control == "right":
            labels.append(3)
        elif control == "rotate_clockwise":
            labels.append(4)
        elif control == "rotate_counter_clockwise":
            labels.append(5)
        elif control == "up":
            labels.append(6)
        elif control == "down":
            labels.append(7)

    video.release()
    return np.array(images), np.array(labels)

# 加载数据
video_path = "C:/TelloMazeNavigation/data/flight_video.avi"  # 视频文件路径
csv_file = "C:/TelloMazeNavigation/data/flight_data.csv"     # 控制指令的CSV文件路径
images, labels = load_data_from_video(video_path, csv_file)

# 构建CNN模型
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(8, activation='softmax')  # 8个控制指令
])

# 编译模型
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 检查数据集的大小并设置训练集和验证集
if len(images) > 1:
    model.fit(images, labels, epochs=10, batch_size=32, validation_split=0.2)
else:
    print("样本数不足以进行训练，请检查数据采集。")

# 保存模型
model.save('C:/TelloMazeNavigation/model/tello_navigation_model.h5')
