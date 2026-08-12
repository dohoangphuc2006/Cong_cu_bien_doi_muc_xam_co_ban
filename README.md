# 🎨 Công Cụ Biến Đổi Mức Xám Cơ Bản (Basic Gray-Level Transformation Tool)

Ứng dụng GUI viết bằng **Python (Tkinter, OpenCV, Matplotlib)** hỗ trợ trực quan hóa và thực hiện các kỹ thuật biến đổi mức xám (Gray-level Transformation) cũng như biến đổi Histogram trên ảnh xám trong Xử lý ảnh kỹ thuật số (Digital Image Processing).

---

## 📌 Tính năng chính

Ứng dụng hỗ trợ **10 thuật toán biến đổi mức xám & Histogram** phổ biến:

1. **Âm bản (Image Negative):** Đảo ngược mức xám.
2. **Biến đổi Log (Log Transformation):** Kéo giãn vùng tối, nén vùng sáng.
3. **Log nghịch đảo (Inverse Log):** Nén vùng tối, mở rộng dải động vùng sáng.
4. **Biến đổi Gamma (Power-Law / Gamma Transformation):** Hiệu chỉnh độ sáng theo hàm lũy thừa.
5. **Phân ngưỡng (Thresholding):** Chuyển ảnh xám thành ảnh nhị phân dựa trên giá trị ngưỡng (Threshold).
6. **Kéo giãn độ tương phản (Contrast Stretching):** Tăng độ tương phản tuyến tính từng đoạn.
7. **Cắt lát mức xám (Gray-level Slicing):** Làm nổi bật dải mức xám $[a, b]$ (có tùy chọn giữ nguyên hoặc xóa nền).
8. **Cân bằng Histogram (Histogram Equalization):** Tự động phân bố lại cường độ mức xám dựa trên hàm CDF.
9. **Cắt lát mặt phẳng Bit (Bit-plane Slicing):** Tách ảnh thành 8 mặt phẳng nhị phân tương ứng từng vị trí bit.
10. **Khớp lược đồ xám (Histogram Matching / Specification):** Biến đổi Histogram của ảnh gốc theo ảnh tham chiếu.

### ✨ Điểm nổi bật về giao diện & trải nghiệm
* **Giao diện hiện đại (GUI Tkinter):** Tự động tùy chỉnh slider / checkbox / nút bấm tùy theo thuật toán được chọn.
* **Tích hợp khung giải thích nguyên lý:** Hiển thị chi tiết mô tả, công thức toán học, ưu/nhược điểm và ứng dụng thực tế cho từng thuật toán.
* **Trực quan hóa sinh động:** Hiển thị đồng thời 4 ô: *Ảnh gốc, Ảnh kết quả, Histogram gốc, Histogram kết quả*[cite: 4].
* **Xử lý tiếng Việt & Đường dẫn:** Hỗ trợ đọc/ghi ảnh với đường dẫn chứa tiếng Việt hoặc ký tự đặc biệt thông qua bộ đệm OpenCV (`imdecode` / `imencode`)[cite: 4].

---

## 📁 Cấu trúc dự án

```text
.
├── main.py          # Controller chính điều khiển luồng dữ liệu và sự kiện ứng dụng
├── giao_dien.py     # Thiết kế giao diện người dùng (GUI) bằng Tkinter & Matplotlib
├── thuat_toan.py    # Định nghĩa các hàm xử lý toán học & biến đổi ảnh xám
└── README.md        # Tài liệu hướng dẫn sử dụng
```
---

## 🛠 Yêu cầu hệ thống & Cài đặt

### 1. Yêu cầu môi trường
* **Python 3.8+**
* **Tkinter** (thường đi kèm sẵn khi cài đặt Python trên Windows)

### 2. Cài đặt các thư viện phụ thuộc
Mở Terminal / Command Prompt và chạy lệnh:

```bash
pip install opencv-python numpy matplotlib
```
---

## 📖 Hướng dẫn sử dụng

1. **Chọn ảnh đầu vào:** Nhấn nút 📂 **Chọn ảnh đầu vào** để tải ảnh cần xử lý.
2. **Chọn thuật toán:** Chọn thuật toán mong muốn tại menu danh sách thả xuống (Combobox).
3. **Tùy chỉnh tham số (nếu có):**
   * Với **Gamma / Phân ngưỡng / Bit-plane**: Kéo slider đơn để thay đổi tham số tương ứng.
   * Với **Contrast Stretching / Gray-level Slicing**: Sử dụng slider đôi để chỉnh ngưỡng thấp ($r_{min}/a$) và ngưỡng cao ($r_{max}/b$).
   * Với **Histogram Matching**: Nhấn nút 📂 **Chọn ảnh tham chiếu** để tải ảnh mẫu.
4. **Xem kết quả:** Ảnh kết quả và Histogram tương ứng sẽ được cập nhật thời gian thực (Real-time).
5. **Lưu ảnh:** Nhấn nút 💾 **Lưu ảnh kết quả** để xuất ảnh ra định dạng PNG hoặc JPEG.
6. **Đặt lại:** Nhấn nút 🔄 **Đặt lại** nếu muốn làm mới ứng dụng về trạng thái ban đầu.

---

## 📜 Giấy phép (License)

Dự án được phát triển phục vụ mục đích học tập và nghiên cứu môn **Xử lý ảnh kỹ thuật số (Digital Image Processing)**.
