import ffmpeg
import cv2
import glob
import os

FOLDER_HEAD = "C:/Users/ElliotLondon/Documents/PythonLocal/S4CSCardington/data"
folders = [
    '2022_03_05/Camera 3',
    '2022_03_09/Camera 3',
    '2022_03_18/Camera 3',
    '2022_04_07/Camera 3',
    '2022_04_07/Camera 6',
    '2022_04_08/Camera 3'
]


def merge_pngs_to_mp4(folder: str):
    # Converts a series of .png files into a mp4 file
    img_array = []
    height = 1860
    width = 2880
    size = (width, height)
    print(os.path.exists(f'{FOLDER_HEAD}/{folder}'))
    _, _, files = next(os.walk(f'{FOLDER_HEAD}/{folder}'))
    file_count = len(files) - 1
    i_tmp = 0
    for filename in glob.glob(f'{FOLDER_HEAD}/{folder}/*.png'):
        if i_tmp % 100 == 0:
            print(f'Processing: {filename}, #: {i_tmp}/{file_count}')
        img = cv2.imread(filename)
        img_array.append(img)
        i_tmp += 1

    out = cv2.VideoWriter(f'{FOLDER_HEAD}/{folder}/timelapse.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

    for i in range(len(img_array)):
        if i % 100 == 0:
            print(f'Writing: {i}/{file_count}')
        out.write(img_array[i])
    out.release()


if __name__ == '__main__':
    for j in folders:
        merge_pngs_to_mp4(j)
    print('All done!')
