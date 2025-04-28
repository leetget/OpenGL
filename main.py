import numpy as np
import matplotlib.pyplot as plt
import cv2

def preprocess(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0) # шумодав
    ycrcb = cv2.cvtColor(blurred, cv2.COLOR_BGR2YCrCb) # YCrCb: Y — яркость (чёрно-белая часть), cr (красный оттенок), cb (синий оттенок)
    y, cr, cb = cv2.split(ycrcb)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) # улучшение контраста
    y = clahe.apply(y)
    corrected = cv2.merge([y, cr, cb])
    corrected = cv2.cvtColor(corrected, cv2.COLOR_YCrCb2BGR)
    gamma_table = np.array([((i / 255.0) ** (1.0 / 1.2)) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(corrected, gamma_table) # применяем гамма-коррекцию с коэффициентом 1.2 (осветляем тёмные области)


def find_corners(image): #ищем горизонтальные и вертикальные линии
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=10)
    if lines is None:
        raise ValueError("Линии не найдены.")
    
    h_lines, v_lines = [], []
    image_with_lines = image.copy()
    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi # Угол наклона линии в радианах
        
        if abs(angle) < 10 or abs(angle - 180) < 10: # Горизонтальные линии: угол близок к 0° или 180° (±10°)
            h_lines.append((x1, y1, x2, y2))
            cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
        elif abs(angle - 90) < 10 or abs(angle + 90) < 10: # Вертикальные линии: угол близок к 90° или -90° (±10°)
            v_lines.append((x1, y1, x2, y2))
            cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    if not h_lines or not v_lines:
        raise ValueError(f"Недостаточно линий: горизонтальных {len(h_lines)}, вертикальных {len(v_lines)}")
    
    corners = []
    for h in h_lines:
        for v in v_lines:
            if h[0] <= v[0] <= h[2] and v[1] <= h[1] <= v[3]:
                corners.append((v[0], h[1]))
    
    print(f"Найдено горизонтальных линий: {len(h_lines)}")
    print(f"Найдено вертикальных линий: {len(v_lines)}")
    print(f"Найдено углов: {len(corners)}")
    if len(corners) < 5:
        raise ValueError(f"Найдено недостаточно углов: {len(corners)}. Требуется минимум 5.")
    
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(edges, cmap='gray')
    plt.title("Обнаруженные края (Canny)")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(image_with_lines, cv2.COLOR_BGR2RGB))
    plt.title("Обнаруженные линии")
    plt.axis('off')
    plt.show()
    
    return corners


def calibrate(corners, size):
    obj_pts = np.zeros((len(corners), 3), np.float32)
    obj_pts[:, :2] = np.array(corners, dtype=np.float32)
    img_pts = np.array(corners, dtype=np.float32).reshape(-1, 1, 2)
    flags = cv2.CALIB_FIX_K3 | cv2.CALIB_FIX_K4 | cv2.CALIB_FIX_K5 | cv2.CALIB_FIX_K6
    ret, mtx, dist, _, _ = cv2.calibrateCamera([obj_pts], [img_pts], size, None, None, flags=flags) # возвращаем матрицу цветов и коэфы дисторсии(mtx&dist)
    if not ret:
        raise ValueError("Калибровка не удалась.")
    return mtx, dist


def undistort(image1, image2, mtx, dist): # удаляем искажения
    return cv2.undistort(image1, mtx, dist), cv2.undistort(image2, mtx, dist)


def show_pair(image, title_img, title_hist):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title_img)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    for i, color in enumerate(('b', 'g', 'r')):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color, label=f'Канал {color.upper()}')
    plt.title(title_hist)
    plt.xlabel("Значение пикселя")
    plt.ylabel("Частота")
    plt.legend()
    plt.grid(True)
    plt.show()


def match_keypoints(img1, img2):
    gray1, gray2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create(nfeatures=1000, contrastThreshold=0.04, edgeThreshold=10)
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    
    if not kp1 or des1 is None or not kp2 or des2 is None:
        raise ValueError("Ключевые точки не найдены.")
    
    flann = cv2.FlannBasedMatcher({'algorithm': 0, 'trees': 5}, {'checks': 50}) # по сути кнн
    matches = flann.knnMatch(des1, des2, k=2)
    
    good = []
    for match in matches:
        if len(match) == 2:
            m, n = match
            if m.distance < 0.7 * n.distance:
                good.append(m)
    
    if len(good) < 4:
        raise ValueError("Недостаточно совпадений.")
    
    result = cv2.drawMatches(img1, kp1, img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(figsize=(15, 8))
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title("Сопоставленные ключевые точки")
    plt.axis('off')
    plt.show()
    
    return kp1, kp2, good


def apply_homography(img1, img2, kp1, kp2, matches): # матрица гомографии между двумя изображениями
    if len(matches) >= 4:
        src = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        if H is not None:
            h, w = img1.shape[:2]
            warped = cv2.warpPerspective(img2, H, (w, h))
            plt.figure(figsize=(10, 5))
            plt.imshow(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
            plt.title("Преобразованное изображение")
            plt.axis('off')
            plt.show()
        else:
            print("Гомография не вычислена.")
    else:
        print("Недостаточно совпадений для гомографии.")


def main():
    try:
        img1 = cv2.imread('image1.jpg')
        img2 = cv2.imread('image2.jpg')
        if img1 is None or img2 is None:
            raise ValueError("Ошибка загрузки изображений.")
        print("Изображения загружены.")
        
        show_pair(img1, "Исходное изображение 1", "Гистограмма исходного изображения 1")
        show_pair(img2, "Исходное изображение 2", "Гистограмма исходного изображения 2")

        processed1, processed2 = preprocess(img1), preprocess(img2)
        print("Обработка завершена.")
        
        show_pair(processed1, "Обработанное изображение 1", "Гистограмма обработанного изображения 1")
        show_pair(processed2, "Обработанное изображение 2", "Гистограмма обработанного изображения 2")

        corners = find_corners(processed1)
        size = img1.shape[:2][::-1]
        mtx, dist = calibrate(corners, size)
        print("Калибровка завершена.")

        undistorted1, undistorted2 = undistort(processed1, processed2, mtx, dist)
        print("Искажения исправлены.")
        
        show_pair(undistorted1, "Исправленное изображение 1", "Гистограмма исправленного изображения 1")
        show_pair(undistorted2, "Исправленное изображение 2", "Гистограмма исправленного изображения 2")

        kp1, kp2, matches = match_keypoints(undistorted1, undistorted2)
        print("Ключевые точки сопоставлены.")

        apply_homography(undistorted1, undistorted2, kp1, kp2, matches)
        print("Преобразование выполнено.")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()