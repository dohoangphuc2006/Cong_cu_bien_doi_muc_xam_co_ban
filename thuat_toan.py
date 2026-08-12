import cv2
import numpy as np


def bien_doi_am_ban(img, L=256):
    return (L - 1) - img


def bien_doi_log(img, L=256):
    r_float = img.astype(float)
    c = (L - 1) / np.log(1.0 + (L - 1))

    s = c * np.log(1.0 + r_float)
    return np.uint8(s)

def bien_doi_histogram_equalization(img):
    return cv2.equalizeHist(img)


def bien_doi_gamma(img, gamma=3.0, c=1.0, L=256):
    if gamma <= 0:
        raise ValueError("Giá trị Gamma phải lớn hơn 0!")

    img_float = img.astype(np.float32)

    r = img_float / (L - 1)
    s = c * np.power(r, gamma)

    result = s * (L - 1)

    result = np.clip(result, 0, L - 1)

    return result.astype(np.uint8)


def bien_doi_phan_nguong(img, thresh_val):
    if thresh_val < 0 or thresh_val > 255:
        raise ValueError("Giá trị ngưỡng phải nằm trong khoảng 0 đến 255!")

    _, thresh_img = cv2.threshold(img, thresh_val, 255, cv2.THRESH_BINARY)
    return thresh_img


def bien_doi_contrast_stretching(img, r_min, r_max, L=256):

    # Kiểm tra tham số hợp lệ: r_min, r_max phải nằm trong khoảng 0 đến L-1
    if r_min < 0 or r_min > (L - 1) or r_max < 0 or r_max > (L - 1):
        raise ValueError(f"Giá trị r_min, r_max phải nằm trong khoảng 0 đến {L - 1}!")

    if r_min >= r_max:
        r_max = r_min + 1
    s1 = 0
    s2 = L - 1

    m1 = s1 / r_min if r_min != 0 else 0
    m2 = (s2 - s1) / (r_max - r_min) if r_min != r_max else 0
    m3 = ((L - 1) - s2) / ((L - 1) - r_max) if r_max != (L - 1) else 0

    mask_1 = (img < r_min).astype(float)
    mask_2 = ((img >= r_min) & (img <= r_max)).astype(float)
    mask_3 = (img > r_max).astype(float)

    im1 = mask_1 * np.floor(m1 * img).astype(float)
    im2 = mask_2 * np.floor(s1 + (m2 * (img - r_min))).astype(float)
    im3 = mask_3 * np.floor(s2 + (m3 * (img - r_max))).astype(float)

    s = np.uint8(im1 + im2 + im3)

    return s


def bien_doi_gray_level_slicing(img, a, b, giu_nen=False, SH=255):
    if a < 0 or a > 255 or b < 0 or b > 255:
        raise ValueError("Giá trị a, b phải nằm trong khoảng 0 đến 255!")

    if a >= b:
        b = a + 1
    mask = (img >= a) & (img <= b)

    if giu_nen:
        res = img.copy()
        res[mask] = SH
    else:
        res = np.zeros_like(img, dtype=np.uint8)
        res[mask] = SH

    return res
def bien_doi_inverse_log(img, L=256):
    r_float = img.astype(float)
    r_norm = r_float / (L - 1)
    c = (L - 1) / 9.0
    s = c * (np.power(10.0, r_norm) - 1.0)
    return np.uint8(np.clip(s, 0, L - 1))

def bien_doi_bit_plane_slicing(img, k):
    if k < 0 or k > 7:
        raise ValueError("Thứ tự mặt phẳng bit k phải nằm trong khoảng từ 0 đến 7!")
        
    bit_plane = (img >> k) & 1
    return np.uint8(bit_plane * 255)


def bien_doi_histogram_matching(img_source, img_ref):
    hist_src, _ = np.histogram(img_source.flatten(), 256, [0, 256])
    hist_ref, _ = np.histogram(img_ref.flatten(), 256, [0, 256])

    cdf_src = hist_src.cumsum()
    cdf_src_norm = cdf_src / float(cdf_src[-1]) if cdf_src[-1] != 0 else cdf_src
    
    cdf_ref = hist_ref.cumsum()
    cdf_ref_norm = cdf_ref / float(cdf_ref[-1]) if cdf_ref[-1] != 0 else cdf_ref

    lut = np.zeros(256, dtype=np.uint8)
    for r in range(256):
        diff = np.abs(cdf_ref_norm - cdf_src_norm[r])
        lut[r] = np.argmin(diff)

    return lut[img_source]