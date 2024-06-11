import gradio as gr
import cv2
import tempfile
import numpy as np
import random

def dummy_yolo_detection(frame):
    # Добавление случайного прямоугольника на кадр для демонстрации
    height, width, _ = frame.shape
    x1, y1 = random.randint(0, width // 2), random.randint(0, height // 2)
    x2, y2 = random.randint(width // 2, width), random.randint(height // 2, height)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def process_video(video_file, frequency):
    # Открытие видеофайла с использованием cv2
    cap = cv2.VideoCapture(video_file.name)
    if not cap.isOpened():
        return "Ошибка открытия видеофайла.", None
    
    frame_count = 0
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    timestamps = []
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frequency == 0:
            # Используем пустышку для обработки кадров
            processed_frame = dummy_yolo_detection(frame)
            frames.append(processed_frame)
            timestamps.append(frame_count / frame_rate)

        frame_count += 1

    cap.release()

    if not frames:
        return "Нет обработанных кадров.", None

    # Создание видео из обработанных кадров
    height, width, layers = frames[0].shape
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    out = cv2.VideoWriter(temp_output.name, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    
    return temp_output.name, np.array(timestamps).reshape(-1, 1)

iface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Загрузите видео"),
        gr.Slider(1, 100, step=1, label="Частота разбиения (кадры)")
    ],
    outputs=[
        gr.Video(label="Обработанное видео"),
        gr.Dataframe(headers=["Временная метка (секунды)"], label="Временные метки")
    ],
    title="Обработка видео",
    description="Загрузите видео, чтобы увидеть временные метки кадров. Частота разбиения указывает, как часто анализировать кадры."
)

iface.launch()