"""
main.py
=======
Controller điều phối toàn bộ chương trình.
Kết nối giao diện (giao_dien.py) với thuật toán (thuat_toan.py).

Luồng hoạt động:
    1. Người dùng chọn ảnh => load_image_event()
    2. Thuật toán/tham số thay đổi => update_ui_and_process()
    3. Xử lý ảnh => process_image()
    4. Cập nhật giao diện => render_plots()
    5. Lưu ảnh => save_image_event()
"""

import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import thuat_toan
from giao_dien import GiaoDien


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        # --- Biến trạng thái ảnh ---
        self.img_original = None   
        self.img_reference = None  
        self.img_processed = None  

        self.ui = GiaoDien(
            root=self.root,
            xu_ly_chon_anh=self.load_image_event,
            xu_ly_bien_doi=self.update_ui_and_process,
            xu_ly_luu_anh=self.save_image_event,
            xu_ly_reset=self.reset_event,
            xu_ly_chon_ref=self.load_ref_image_event
        )

    # =========================================================
    # 1. XỬ LÝ SỰ KIỆN CHÍNH TỪ GIAO DIỆN
    # =========================================================

    def load_image_event(self):
        duong_dan = filedialog.askopenfilename(
            title="Chọn ảnh đầu vào",
            filetypes=[
                ("Tệp ảnh", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp"),
                ("Tất cả tệp", "*.*")
            ]
        )
        if not duong_dan:
            return
        try:
            with open(duong_dan, "rb") as f:
                file_bytes = f.read()
            import numpy as np
            arr = np.frombuffer(file_bytes, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
            if img is not None and img.ndim == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except Exception:
            img = None
        if img is None:
            messagebox.showerror(
                "Lỗi",
                "Không thể đọc file ảnh!\nVui lòng chọn file ảnh hợp lệ."
            )
            return
        self.img_original = img
        ten_file = duong_dan.split("/")[-1].split("\\")[-1]
        self.ui.cap_nhat_ten_file(ten_file)

        self.update_ui_and_process()

    def load_ref_image_event(self):

        duong_dan = filedialog.askopenfilename(
            title="Chọn ảnh tham chiếu",
            filetypes=[
                ("Tệp ảnh", "*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.webp"),
                ("Tất cả tệp", "*.*")
            ]
        )

        if not duong_dan:
            return

        try:
            with open(duong_dan, "rb") as f:
                file_bytes = f.read()
            import numpy as np
            arr = np.frombuffer(file_bytes, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
            if img is not None and img.ndim == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except Exception:
            img = None

        if img is None:
            messagebox.showerror(
                "Lỗi",
                "Không thể đọc file ảnh tham chiếu!\nVui lòng chọn file ảnh hợp lệ."
            )
            return

        self.img_reference = img
        ten_file = duong_dan.split("/")[-1].split("\\")[-1]
        self.ui.cap_nhat_ten_file_ref(ten_file)
        self.update_ui_and_process()

    # =========================================================
    # 2. CẬP NHẬT GIAO DIỆN VÀ CHUẨN BỊ XỬ LÝ
    # =========================================================

    def update_ui_and_process(self):
        if self.img_original is not None:
            self.ui.hien_giai_thich()
        else:
            self.ui.an_giai_thich()

        ten_thuat_toan = self.ui.lay_thuat_toan()

        if ten_thuat_toan == "Gamma":
            # Cấu hình slider cho Gamma
            self.ui.cap_nhat_slider(
                from_=0.1, to=5.0, resolution=0.1,
                gia_tri_mac_dinh=self.ui.lay_gia_tri_slider(),
                nhan="Gamma"
            )
            self.ui.hien_slider()

        elif ten_thuat_toan == "Phân ngưỡng":
            # Cấu hình slider cho Ngưỡng
            self.ui.cap_nhat_slider(
                from_=0, to=255, resolution=1,
                gia_tri_mac_dinh=self.ui.lay_gia_tri_slider(),
                nhan="Ngưỡng"
            )
            self.ui.hien_slider()

        elif ten_thuat_toan == "Cắt lát mặt phẳng bit":
            cur_val = self.ui.lay_gia_tri_slider()
            val = int(cur_val) if 0 <= cur_val <= 7 else 7
            self.ui.cap_nhat_slider(
                from_=0, to=7, resolution=1,
                gia_tri_mac_dinh=val,
                nhan="Bit plane"
            )
            self.ui.hien_slider()

        else:
            self.ui.an_slider()
        self.process_image()

    # =========================================================
    # 3. XỬ LÝ ẢNH (GỌI THUẬT TOÁN)
    # =========================================================

    def process_image(self):

        if self.img_original is None:
            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn ảnh đầu vào trước!"
            )
            return
        ten_thuat_toan = self.ui.lay_thuat_toan()
        try:
            if ten_thuat_toan == "Âm bản":
                self.img_processed = thuat_toan.bien_doi_am_ban(self.img_original)

            elif ten_thuat_toan == "Log":

                self.img_processed = thuat_toan.bien_doi_log(self.img_original)

            elif ten_thuat_toan == "Log nghịch đảo":

                self.img_processed = thuat_toan.bien_doi_inverse_log(self.img_original)

            elif ten_thuat_toan == "Gamma":

                gamma_val = float(self.ui.lay_gia_tri_slider())
                self.img_processed = thuat_toan.bien_doi_gamma(self.img_original, gamma=gamma_val)

            elif ten_thuat_toan == "Phân ngưỡng":

                thresh_val = int(self.ui.lay_gia_tri_slider())
                self.img_processed = thuat_toan.bien_doi_phan_nguong(self.img_original, thresh_val)

            elif ten_thuat_toan == "Cắt lát mặt phẳng bit":

                k_val = int(self.ui.lay_gia_tri_slider())
                self.img_processed = thuat_toan.bien_doi_bit_plane_slicing(self.img_original, k_val)

            elif ten_thuat_toan == "Histogram Matching":
                if self.img_reference is None:
                    messagebox.showwarning(
                        "Thông báo",
                        "Vui lòng chọn ảnh tham chiếu trước!"
                    )
                    return
                self.img_processed = thuat_toan.bien_doi_histogram_matching(
                    self.img_original, self.img_reference
                )

            elif ten_thuat_toan == "Contrast Stretching":

                r_min, r_max = self.ui.lay_gia_tri_slider_doi()
                self.img_processed = thuat_toan.bien_doi_contrast_stretching(
                    self.img_original, r_min, r_max
                )

            elif ten_thuat_toan == "Gray-level Slicing":

                a, b = self.ui.lay_gia_tri_slider_doi()

                giu_nen = self.ui.lay_giu_nen()
                self.img_processed = thuat_toan.bien_doi_gray_level_slicing(
                    self.img_original, a, b, giu_nen
                )

            elif ten_thuat_toan == "Histogram Equalization":
                self.img_processed = thuat_toan.bien_doi_histogram_equalization(self.img_original)

            else:
                messagebox.showerror("Lỗi", f"Thuật toán không hợp lệ: {ten_thuat_toan}")
                return

        except ValueError as loi:

            messagebox.showerror("Lỗi tham số", str(loi))
            return

        except Exception as loi:

            messagebox.showerror(
                "Lỗi xử lý ảnh",
                f"Đã xảy ra lỗi khi xử lý ảnh:\n{loi}"
            )
            return
        self.render_plots()

    # =========================================================
    # 4. VẼ LẠI 4 Ô MATPLOTLIB
    # =========================================================

    def render_plots(self):
        axes = self.ui.axes
        canvas = self.ui.canvas
        for ax in axes.ravel():
            ax.clear()

        axes[0, 0].imshow(self.img_original, cmap='gray', vmin=0, vmax=255)
        axes[0, 0].set_title("Original Image", fontsize=11, fontweight='bold', color="#2c3e50")
        axes[0, 0].axis('off')  # Ẩn trục toạ độ

        axes[0, 1].imshow(self.img_processed, cmap='gray', vmin=0, vmax=255)
        # Tên thuật toán hiện tại
        ten_thuat_toan = self.ui.lay_thuat_toan()
        axes[0, 1].set_title(
            f"Processed Image  [{ten_thuat_toan}]",
            fontsize=11, fontweight='bold', color="#27ae60"
        )
        axes[0, 1].axis('off')

        axes[1, 0].hist(
            self.img_original.ravel(), 
            bins=256,
            range=(0, 256),
            color="#3498db",
            alpha=0.8
        )
        axes[1, 0].set_title("Original Histogram", fontsize=11, fontweight='bold', color="#2c3e50")
        axes[1, 0].set_xlabel("Cường độ pixel (0–255)", fontsize=8)
        axes[1, 0].set_ylabel("Số lượng pixel", fontsize=8)
        axes[1, 0].set_xlim([0, 256])
        axes[1, 0].tick_params(labelsize=7)

        # --- Ô [1,1]: Histogram ảnh kết quả ---
        axes[1, 1].hist(
            self.img_processed.ravel(),
            bins=256,
            range=(0, 256),
            color="#27ae60",
            alpha=0.8
        )
        axes[1, 1].set_title("Processed Histogram", fontsize=11, fontweight='bold', color="#27ae60")
        axes[1, 1].set_xlabel("Cường độ pixel (0–255)", fontsize=8)
        axes[1, 1].set_ylabel("Số lượng pixel", fontsize=8)
        axes[1, 1].set_xlim([0, 256])
        axes[1, 1].tick_params(labelsize=7)

        canvas.draw()

    # =========================================================
    # 5. LƯU ẢNH KẾT QUẢ
    # =========================================================

    def save_image_event(self):

        if self.img_processed is None:
            messagebox.showwarning(
                "Thông báo",
                "Chưa có ảnh kết quả để lưu!\nVui lòng chọn ảnh và áp dụng thuật toán trước."
            )
            return

        # Mở hộp thoại lưu file
        duong_dan_luu = filedialog.asksaveasfilename(
            title="Lưu ảnh kết quả",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("JPEG", "*.jpeg"),
                ("Tất cả tệp", "*.*")
            ]
        )
        if not duong_dan_luu:
            return

        try:
            duoi_file = duong_dan_luu.lower().split(".")[-1]
            ext = "." + duoi_file if duoi_file in ("png", "jpg", "jpeg") else ".png"
            ket_qua, buffer = cv2.imencode(ext, self.img_processed)
            if ket_qua:
                with open(duong_dan_luu, "wb") as f:
                    f.write(buffer.tobytes())
        except Exception:
            ket_qua = False

        if ket_qua:
            messagebox.showinfo(
                "Thành công",
                f"Lưu ảnh thành công!\n{duong_dan_luu}"
            )
        else:
            messagebox.showerror(
                "Lỗi",
                "Lưu ảnh thất bại!\nVui lòng kiểm tra đường dẫn và quyền ghi file."
            )


    # =========================================================
    # 6. ĐẶT LẠI ỨNG DỤNG VỀ TRẠNG THÁI BAN ĐẦU
    # =========================================================

    def reset_event(self):

        self.img_original = None
        self.img_reference = None
        self.img_processed = None
        self.ui.dat_lai_giao_dien()


# =========================================================
# KHỐI THỰC THI CHÍNH
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()