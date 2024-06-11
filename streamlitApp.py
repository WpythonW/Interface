import streamlit as st
import os

# Создание папки для загрузки файлов
if not os.path.exists("uploaded_files"):
    os.makedirs("uploaded_files")

# Функция для загрузки файлов
def save_uploaded_file(uploaded_file):
    with open(os.path.join("uploaded_files", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

# Функция для получения списка всех файлов в папке
def get_all_files():
    return os.listdir('uploaded_files')

# Заголовок приложения
st.title("Загрузите фото и видео, затем выберите файл из списка")

# Загрузка файлов
uploaded_files = st.file_uploader("Загрузите фото и видео", accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        save_uploaded_file(uploaded_file)
    st.success("Файлы загружены")

# Получение всех файлов в папке
all_files = get_all_files()

# Поле для выбора файла из выпадающего списка
selected_file = st.selectbox("Выберите файл", all_files)
if selected_file:
    st.write(f"Вы выбрали файл: {selected_file}")

# Отображение выбранного файла
if selected_file and selected_file.endswith('.mp4'):
    st.video(os.path.join('uploaded_files', selected_file))
elif selected_file:
    st.image(os.path.join('uploaded_files', selected_file))
