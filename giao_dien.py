import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GiaoDien:
    def __init__(self, root, xu_ly_chon_anh, xu_ly_bien_doi, xu_ly_luu_anh, xu_ly_reset, xu_ly_chon_ref):
        self.root = root
        self.xu_ly_chon_anh  = xu_ly_chon_anh
        self.xu_ly_bien_doi  = xu_ly_bien_doi
        self.xu_ly_luu_anh   = xu_ly_luu_anh
        self.xu_ly_reset     = xu_ly_reset
        self.xu_ly_chon_ref  = xu_ly_chon_ref

        # --- Thiết lập cửa sổ chính ---
        self.root.title("CÔNG CỤ BIẾN ĐỔI MỨC XÁM CƠ BẢN")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        # --- Biến trạng thái giao diện ---
        self.ten_file_var    = tk.StringVar(value="Chưa chọn ảnh")
        self.thuat_toan_var  = tk.StringVar(value="Âm bản")

        # Slider đơn (Gamma, Phân ngưỡng)
        self.slider_val      = tk.DoubleVar(value=1.0)
        self.slider_label_var = tk.StringVar(value="")

        # Slider đôi — dùng cho Contrast Stretching & Gray-level Slicing
        self.slider_low_val  = tk.DoubleVar(value=50.0)
        self.slider_high_val = tk.DoubleVar(value=200.0)

        # Checkbox "Giữ nguyên nền" cho Gray-level Slicing
        self.giu_nen_var     = tk.BooleanVar(value=False)

        self._tao_control_panel()
        self._tao_khu_vuc_hien_thi()

    # =========================================================
    # PHẦN 1: CONTROL PANEL
    # =========================================================

    def _tao_control_panel(self):
        self.frame_control = tk.Frame(
            self.root, bg="#2c3e50", width=230, padx=12, pady=15
        )
        self.frame_control.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_control.pack_propagate(False)

        # Tiêu đề
        tk.Label(
            self.frame_control, text="⚙ ĐIỀU KHIỂN",
            bg="#2c3e50", fg="#ecf0f1", font=("Arial", 12, "bold")
        ).pack(pady=(0, 15))

        # Nút chọn ảnh
        tk.Button(
            self.frame_control, text="📂  Chọn ảnh đầu vào",
            command=self.xu_ly_chon_anh,
            bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", padx=8, pady=6
        ).pack(fill=tk.X, pady=(0, 6))

        # Nhãn tên file
        tk.Label(
            self.frame_control, textvariable=self.ten_file_var,
            bg="#34495e", fg="#bdc3c7", font=("Arial", 8),
            wraplength=200, justify=tk.CENTER, padx=4, pady=4
        ).pack(fill=tk.X, pady=(0, 14))

        # Nhãn chọn thuật toán
        tk.Label(
            self.frame_control, text="Chọn thuật toán:",
            bg="#2c3e50", fg="#ecf0f1", font=("Arial", 10)
        ).pack(anchor=tk.W, pady=(0, 4))

        # Combobox — 6 thuật toán
        self.combo_thuat_toan = ttk.Combobox(
            self.frame_control,
            textvariable=self.thuat_toan_var,
            values=[
                "Âm bản",
                "Log",
                "Log nghịch đảo",
                "Gamma",
                "Phân ngưỡng",
                "Contrast Stretching",
                "Gray-level Slicing",
                "Histogram Equalization",
                "Cắt lát mặt phẳng bit",
                "Histogram Matching",
            ],
            state="readonly", font=("Arial", 10), width=20
        )
        self.combo_thuat_toan.pack(fill=tk.X, pady=(0, 8))
        self.combo_thuat_toan.bind("<<ComboboxSelected>>", self._khi_doi_thuat_toan)

        # ---- Khung giải thích nguyên lý thuật toán ----
        # Hiển thị đầy đủ: Tên, Mô tả, Công thức, Ứng dụng, Ưu điểm, Nhược điểm
        self.frame_giai_thich = tk.Frame(self.frame_control, bg="#34495e", relief=tk.GROOVE, bd=1)
        self.frame_giai_thich.pack(fill=tk.BOTH, expand=True, pady=(0, 14))

        tk.Label(
            self.frame_giai_thich, text="💡 Nguyên lý thuật toán:",
            bg="#34495e", fg="#f39c12", font=("Arial", 9, "bold")
        ).pack(anchor=tk.W, padx=6, pady=(4, 2))

        # Khung con chứa Text + Scrollbar (nội dung dài nên cần cuộn)
        self.frame_giai_thich_noi_dung = tk.Frame(self.frame_giai_thich, bg="#34495e")
        self.frame_giai_thich_noi_dung.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        self.scroll_giai_thich = tk.Scrollbar(self.frame_giai_thich_noi_dung)
        self.scroll_giai_thich.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_giai_thich = tk.Text(
            self.frame_giai_thich_noi_dung, bg="#34495e", fg="#ecf0f1",
            font=("Arial", 8), wrap=tk.WORD, height=14, bd=0,
            highlightthickness=0, padx=2, pady=2,
            yscrollcommand=self.scroll_giai_thich.set
        )
        self.txt_giai_thich.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_giai_thich.config(command=self.txt_giai_thich.yview)

        # Khung chỉ để hiển thị (người dùng không được sửa nội dung)
        self.txt_giai_thich.config(state=tk.DISABLED)

        # ---- Frame slider ĐƠN (Gamma / Phân ngưỡng) ----
        self.frame_slider = tk.Frame(self.frame_control, bg="#2c3e50")
        tk.Label(
            self.frame_slider, textvariable=self.slider_label_var,
            bg="#2c3e50", fg="#f39c12", font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 2))
        self.slider = tk.Scale(
            self.frame_slider, variable=self.slider_val,
            orient=tk.HORIZONTAL, from_=0.1, to=5.0, resolution=0.1,
            length=200, bg="#2c3e50", fg="#ecf0f1",
            troughcolor="#7f8c8d", highlightthickness=0,
            command=self._khi_keo_slider
        )
        self.slider.pack(fill=tk.X)

        # ---- Frame slider ĐÔI (Contrast Stretching / Gray-level Slicing) ----
        self.frame_slider_doi = tk.Frame(self.frame_control, bg="#2c3e50")

        # Slider Low
        tk.Label(
            self.frame_slider_doi, text="Ngưỡng thấp (r_min / Low):",
            bg="#2c3e50", fg="#f39c12", font=("Arial", 9, "bold")
        ).pack(anchor=tk.W, pady=(0, 2))
        self.lbl_low = tk.Label(
            self.frame_slider_doi, text="50",
            bg="#2c3e50", fg="#ecf0f1", font=("Arial", 9)
        )
        self.lbl_low.pack(anchor=tk.E)
        self.slider_low = tk.Scale(
            self.frame_slider_doi, variable=self.slider_low_val,
            orient=tk.HORIZONTAL, from_=0, to=254, resolution=1,
            length=200, bg="#2c3e50", fg="#ecf0f1",
            troughcolor="#2980b9", highlightthickness=0,
            command=self._khi_keo_slider_doi
        )
        self.slider_low.pack(fill=tk.X)

        # Slider High
        tk.Label(
            self.frame_slider_doi, text="Ngưỡng cao (r_max / High):",
            bg="#2c3e50", fg="#f39c12", font=("Arial", 9, "bold")
        ).pack(anchor=tk.W, pady=(6, 2))
        self.lbl_high = tk.Label(
            self.frame_slider_doi, text="200",
            bg="#2c3e50", fg="#ecf0f1", font=("Arial", 9)
        )
        self.lbl_high.pack(anchor=tk.E)
        self.slider_high = tk.Scale(
            self.frame_slider_doi, variable=self.slider_high_val,
            orient=tk.HORIZONTAL, from_=1, to=255, resolution=1,
            length=200, bg="#2c3e50", fg="#ecf0f1",
            troughcolor="#e74c3c", highlightthickness=0,
            command=self._khi_keo_slider_doi
        )
        self.slider_high.pack(fill=tk.X)

        # Checkbox "Giữ nguyên nền" — chỉ hiện khi Gray-level Slicing
        self.frame_checkbox = tk.Frame(self.frame_control, bg="#2c3e50")
        self.chk_giu_nen = tk.Checkbutton(
            self.frame_checkbox,
            text="Giữ nguyên nền",
            variable=self.giu_nen_var,
            command=self.xu_ly_bien_doi,
            bg="#2c3e50", fg="#ecf0f1",
            selectcolor="#34495e",
            activebackground="#2c3e50",
            activeforeground="#ecf0f1",
            font=("Arial", 9)
        )
        self.chk_giu_nen.pack(anchor=tk.W, pady=(6, 0))

        # ---- Frame chọn ảnh tham chiếu (chỉ hiện khi Histogram Matching) ----
        self.frame_ref_image = tk.Frame(self.frame_control, bg="#2c3e50")
        self.btn_chon_ref = tk.Button(
            self.frame_ref_image, text="📂  Chọn ảnh tham chiếu",
            command=self.xu_ly_chon_ref,
            bg="#9b59b6", fg="white", font=("Arial", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", padx=8, pady=6
        )
        self.btn_chon_ref.pack(fill=tk.X, pady=(0, 4))
        
        self.ten_file_ref_var = tk.StringVar(value="Chưa chọn ảnh tham chiếu")
        self.lbl_ten_file_ref = tk.Label(
            self.frame_ref_image, textvariable=self.ten_file_ref_var,
            bg="#34495e", fg="#bdc3c7", font=("Arial", 8),
            wraplength=200, justify=tk.CENTER, padx=4, pady=4
        )
        self.lbl_ten_file_ref.pack(fill=tk.X)

        # Đường kẻ phân cách
        tk.Frame(self.frame_control, bg="#7f8c8d", height=1).pack(fill=tk.X, pady=12)

        # Nút lưu ảnh
        tk.Button(
            self.frame_control, text="💾  Lưu ảnh kết quả",
            command=self.xu_ly_luu_anh,
            bg="#2980b9", fg="white", font=("Arial", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", padx=8, pady=6
        ).pack(fill=tk.X, pady=(0, 6))

        # Nút đặt lại (reset) ứng dụng về trạng thái ban đầu
        tk.Button(
            self.frame_control, text="🔄  Đặt lại",
            command=self.xu_ly_reset,
            bg="#e67e22", fg="white", font=("Arial", 10, "bold"),
            relief=tk.FLAT, cursor="hand2", padx=8, pady=6
        ).pack(fill=tk.X)

        # Trạng thái ban đầu: ẩn hết slider và khung giải thích
        self.an_slider()
        self.an_slider_doi()
        self.an_checkbox()
        self.an_chon_ref()
        self.an_giai_thich()

        # Hiển thị sẵn nguyên lý của thuật toán đang chọn mặc định
        self._cap_nhat_giai_thich(self.thuat_toan_var.get())

    # =========================================================
    # PHẦN 2: KHU VỰC HIỂN THỊ
    # =========================================================

    def _tao_khu_vuc_hien_thi(self):
        self.frame_hien_thi = tk.Frame(self.root, bg="#ecf0f1")
        self.frame_hien_thi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 7))
        self.fig.patch.set_facecolor("#ecf0f1")
        self.fig.subplots_adjust(hspace=0.35, wspace=0.25)

        self.axes[0, 0].set_title("Original Image",       fontsize=11, fontweight='bold', color="#2c3e50")
        self.axes[0, 1].set_title("Processed Image",      fontsize=11, fontweight='bold', color="#2c3e50")
        self.axes[1, 0].set_title("Original Histogram",   fontsize=11, fontweight='bold', color="#2c3e50")
        self.axes[1, 1].set_title("Processed Histogram",  fontsize=11, fontweight='bold', color="#2c3e50")

        for ax in self.axes.ravel():
            ax.axis('off')
            ax.set_facecolor("#dfe6e9")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_hien_thi)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # =========================================================
    # PHẦN 3: XỬ LÝ SỰ KIỆN
    # =========================================================

    def _khi_doi_thuat_toan(self, event=None):
        ten = self.thuat_toan_var.get()

        # Ẩn hết trước
        self.an_slider()
        self.an_slider_doi()
        self.an_checkbox()
        self.an_chon_ref()

        # Cập nhật giải thích tác dụng
        self._cap_nhat_giai_thich(ten)

        if ten == "Gamma":
            self.cap_nhat_slider(from_=0.1, to=5.0, resolution=0.1,
                                 gia_tri_mac_dinh=1.0, nhan="Gamma")
            self.hien_slider()

        elif ten == "Phân ngưỡng":
            self.cap_nhat_slider(from_=0, to=255, resolution=1,
                                 gia_tri_mac_dinh=128, nhan="Ngưỡng")
            self.hien_slider()

        elif ten == "Cắt lát mặt phẳng bit":
            self.cap_nhat_slider(from_=0, to=7, resolution=1,
                                 gia_tri_mac_dinh=7, nhan="Bit plane")
            self.hien_slider()

        elif ten == "Histogram Matching":
            self.hien_chon_ref()

        elif ten == "Contrast Stretching":
            self.slider_low_val.set(50)
            self.slider_high_val.set(200)
            self.lbl_low.config(text="50")
            self.lbl_high.config(text="200")
            self.hien_slider_doi()

        elif ten == "Gray-level Slicing":
            self.slider_low_val.set(100)
            self.slider_high_val.set(180)
            self.lbl_low.config(text="100")
            self.lbl_high.config(text="180")
            self.hien_slider_doi()
            self.hien_checkbox()

        # Âm bản / Log / Log nghịch đảo / Histogram Equalization: không slider nào

        self.xu_ly_bien_doi()

    def _khi_keo_slider(self, gia_tri):
        """Slider đơn — Gamma / Phân ngưỡng / Cắt lát mặt phẳng bit."""
        ten = self.thuat_toan_var.get()
        if ten == "Gamma":
            self.slider_label_var.set(f"Gamma: {float(gia_tri):.1f}")
        elif ten == "Phân ngưỡng":
            self.slider_label_var.set(f"Ngưỡng: {int(float(gia_tri))}")
        elif ten == "Cắt lát mặt phẳng bit":
            self.slider_label_var.set(f"Mặt phẳng bit: {int(float(gia_tri))}")
        self.xu_ly_bien_doi()

    def _khi_keo_slider_doi(self, gia_tri=None):
        """Slider đôi — Contrast Stretching / Gray-level Slicing."""
        low  = int(self.slider_low_val.get())
        high = int(self.slider_high_val.get())

        # Đảm bảo low < high
        if low >= high:
            low = high - 1
            self.slider_low_val.set(low)

        self.lbl_low.config(text=str(low))
        self.lbl_high.config(text=str(high))
        self.xu_ly_bien_doi()

    # =========================================================
    # PHẦN 4: TIỆN ÍCH ẨN/HIỆN & LẤY GIÁ TRỊ
    # =========================================================

    def _cap_nhat_giai_thich(self, ten_thuat_toan):
        cac_giai_thich = {
            "Âm bản":
                "📌 Tên: Biến đổi Âm bản (Negative)\n\n"
                "📖 Mô tả: Đảo ngược cường độ sáng của toàn bộ ảnh, "
                "vùng sáng thành tối và vùng tối thành sáng.\n\n"
                "🧮 Công thức: s = (L-1) - r\n\n"
                "🎯 Ứng dụng: Làm nổi bật chi tiết trong vùng tối; "
                "phân tích ảnh y tế (X-ray, MRI).\n\n"
                "✅ Ưu điểm: Đơn giản, tính toán nhanh, không cần "
                "chọn tham số.\n\n"
                "⚠️ Nhược điểm: Chỉ đảo ngược đơn thuần, không tăng "
                "cường được chi tiết trong một dải cường độ hẹp.",

            "Log":
                "📌 Tên: Biến đổi Logarithm (Log Transformation)\n\n"
                "📖 Mô tả: Nén dải động, kéo giãn các giá trị cường "
                "độ thấp (làm sáng vùng tối) và nén các giá trị cường "
                "độ cao (làm tối vùng sáng).\n\n"
                "🧮 Công thức: s = c·log(1+r), với c = (L-1)/log(L)\n\n"
                "🎯 Ứng dụng: Xử lý phổ Fourier; ảnh có dải động rất "
                "lớn (ví dụ ảnh y tế).\n\n"
                "✅ Ưu điểm: Làm nổi bật chi tiết vùng tối hiệu quả "
                "mà không cần chọn tham số.\n\n"
                "⚠️ Nhược điểm: Có thể làm mất chi tiết ở vùng sáng "
                "do bị nén mạnh; khó kiểm soát mức độ biến đổi.",

            "Log nghịch đảo":
                "📌 Tên: Biến đổi Log nghịch đảo (Inverse Log)\n\n"
                "📖 Mô tả: Trái ngược với biến đổi Log, biến đổi này "
                "nén dải động ở mức xám thấp (vùng tối) và mở rộng "
                "dải động ở mức xám cao (vùng sáng).\n\n"
                "🧮 Công thức: s = c·(10^r - 1) với r đã chuẩn hóa về [0,1], "
                "c = (L-1)/9\n\n"
                "🎯 Ứng dụng: Làm nổi bật chi tiết ở vùng sáng; "
                "xử lý ảnh bị lệch dải động về phía sáng.\n\n"
                "✅ Ưu điểm: Tăng cường độ tương phản cho vùng sáng "
                "rất hiệu quả.\n\n"
                "⚠️ Nhược điểm: Làm mất chi tiết ở vùng tối do bị nén mạnh.",

            "Gamma":
                "📌 Tên: Biến đổi Gamma (Power-Law)\n\n"
                "📖 Mô tả: Hiệu chỉnh độ sáng theo hàm lũy thừa. "
                "γ < 1 làm sáng ảnh (kéo giãn vùng tối), γ > 1 làm "
                "tối ảnh (nén vùng sáng).\n\n"
                "🧮 Công thức: s = c·r^γ (r đã chuẩn hóa về [0,1])\n\n"
                "🎯 Ứng dụng: Hiệu chỉnh gamma màn hình/máy in; điều "
                "chỉnh ảnh quá tối hoặc quá sáng.\n\n"
                "✅ Ưu điểm: Linh hoạt, chỉ một tham số γ điều khiển "
                "được cả làm sáng lẫn làm tối.\n\n"
                "⚠️ Nhược điểm: Cần chọn γ phù hợp bằng thử nghiệm; "
                "γ ≤ 0 không hợp lệ về mặt toán học.",

            "Phân ngưỡng":
                "📌 Tên: Phân ngưỡng (Thresholding)\n\n"
                "📖 Mô tả: Chuyển ảnh xám thành ảnh nhị phân đen-trắng "
                "dựa trên một ngưỡng cường độ.\n\n"
                "🧮 Công thức: s = 255 nếu r > ngưỡng; s = 0 nếu "
                "r ≤ ngưỡng\n\n"
                "🎯 Ứng dụng: Phân đoạn ảnh; tách vật thể khỏi nền; "
                "nhận dạng văn bản (OCR).\n\n"
                "✅ Ưu điểm: Đơn giản, nhanh, hiệu quả khi vật thể "
                "và nền có độ tương phản rõ.\n\n"
                "⚠️ Nhược điểm: Mất toàn bộ chi tiết mức xám; nhạy "
                "với việc chọn ngưỡng và ánh sáng không đều.",

            "Contrast Stretching":
                "📌 Tên: Kéo giãn độ tương phản (Contrast Stretching)\n\n"
                "📖 Mô tả: Kéo giãn tuyến tính từng đoạn dải cường độ "
                "[r_min, r_max] ra toàn bộ dải [0, L-1].\n\n"
                "🧮 Công thức: 3 đoạn tuyến tính — r<r_min: s=0; "
                "r_min≤r≤r_max: s=(r-r_min)/(r_max-r_min)·(L-1); "
                "r>r_max: s=L-1\n\n"
                "🎯 Ứng dụng: Cải thiện ảnh chụp thiếu sáng hoặc kém "
                "tương phản.\n\n"
                "✅ Ưu điểm: Tăng tương phản hiệu quả mà vẫn giữ "
                "đúng thứ tự cường độ gốc.\n\n"
                "⚠️ Nhược điểm: Kết quả phụ thuộc nhiều vào việc chọn "
                "r_min, r_max; chọn sai có thể làm mất chi tiết.",

            "Gray-level Slicing":
                "📌 Tên: Lát cắt mức xám (Gray-level Slicing)\n\n"
                "📖 Mô tả: Làm nổi bật một dải mức xám [a, b] cụ thể, "
                "có thể giữ nguyên hoặc xóa nền.\n\n"
                "🧮 Công thức: s = SH nếu a≤r≤b; ngoài dải s = 0 "
                "(xóa nền) hoặc s = r (giữ nền)\n\n"
                "🎯 Ứng dụng: Y tế (tách mô); công nghiệp (phát hiện "
                "lỗi/dị vật); viễn thám.\n\n"
                "✅ Ưu điểm: Khoanh vùng chính xác một dải cường độ "
                "đang quan tâm.\n\n"
                "⚠️ Nhược điểm: Cần biết trước dải [a, b] cần khoanh; "
                "không tự động xác định.",

            "Histogram Equalization":
                "📌 Tên: Cân bằng Histogram (Histogram Equalization)\n\n"
                "📖 Mô tả: Phân bố lại cường độ ảnh theo hàm phân "
                "phối tích lũy (CDF) để tăng tương phản tổng thể.\n\n"
                "🧮 Công thức: s = CDF(r) · (L-1)\n\n"
                "🎯 Ứng dụng: Ảnh mờ, kém tương phản; ảnh y tế, ảnh "
                "thiên văn.\n\n"
                "✅ Ưu điểm: Tự động, không cần chọn tham số, hiệu "
                "quả với nhiều loại ảnh.\n\n"
                "⚠️ Nhược điểm: Có thể khuếch đại nhiễu ở vùng đồng "
                "nhất; đôi khi làm ảnh trông thiếu tự nhiên.",

            "Cắt lát mặt phẳng bit":
                "📌 Tên: Cắt lát mặt phẳng bit (Bit Plane Slicing)\n\n"
                "📖 Mô tả: Tách ảnh mức xám (8-bit) thành 8 mặt phẳng nhị phân "
                "tương ứng với từng vị trí bit từ 0 (LSB) đến 7 (MSB).\n\n"
                "🧮 Công thức: s = 255·((r >> k) & 1) với k ∈ [0, 7]\n\n"
                "🎯 Ứng dụng: Nén ảnh (chỉ giữ lại các bit cao); giấu tin "
                "trong ảnh (steganography bằng LSB).\n\n"
                "✅ Ưu điểm: Giúp phân tích cấu trúc đóng góp thông tin "
                "chi tiết của từng bit.\n\n"
                "⚠️ Nhược điểm: Kết quả trả về là ảnh nhị phân nên mất "
                "đi dải màu xám mịn.",

            "Histogram Matching":
                "📌 Tên: Khớp lược đồ xám (Histogram Matching)\n\n"
                "📖 Mô tả: Biến đổi phân bố lược đồ xám của ảnh gốc sao cho "
                "hình dạng của nó tiệm cận với lược đồ xám của ảnh tham chiếu.\n\n"
                "🧮 Công thức: Biến đổi thông qua CDF của ảnh gốc và ảnh tham chiếu: "
                "z = G^-1(S(r))\n\n"
                "🎯 Ứng dụng: Chuẩn hóa điều kiện ánh sáng giữa các ảnh chụp khác nhau "
                "(vệ tinh, y tế, ghép mảnh).\n\n"
                "✅ Ưu điểm: Kiểm soát được phân bố độ tương phản mong muốn thông qua ảnh tham chiếu mẫu.\n\n"
                "⚠️ Nhược điểm: Phụ thuộc nhiều vào chất lượng và sự tương đồng của ảnh tham chiếu.",
        }

        text = cac_giai_thich.get(ten_thuat_toan, "")

        # Text widget phải mở khóa (NORMAL) mới ghi được nội dung,
        # sau đó khóa lại (DISABLED) để người dùng không sửa được
        self.txt_giai_thich.config(state=tk.NORMAL)
        self.txt_giai_thich.delete("1.0", tk.END)
        self.txt_giai_thich.insert(tk.END, text)
        self.txt_giai_thich.config(state=tk.DISABLED)

    def hien_slider(self):
        self.frame_slider.pack(fill=tk.X, pady=(0, 8))

    def an_slider(self):
        self.frame_slider.pack_forget()

    def hien_slider_doi(self):
        self.frame_slider_doi.pack(fill=tk.X, pady=(0, 8))

    def an_slider_doi(self):
        self.frame_slider_doi.pack_forget()

    def hien_checkbox(self):
        self.frame_checkbox.pack(fill=tk.X)

    def an_checkbox(self):
        self.frame_checkbox.pack_forget()

    def hien_giai_thich(self):
        if self.frame_ref_image.winfo_manager() == "pack":
            self.frame_giai_thich.pack(fill=tk.BOTH, expand=True, pady=(0, 14), after=self.frame_ref_image)
        else:
            self.frame_giai_thich.pack(fill=tk.BOTH, expand=True, pady=(0, 14), after=self.combo_thuat_toan)

    def an_giai_thich(self):
        self.frame_giai_thich.pack_forget()

    def hien_chon_ref(self):
        self.frame_ref_image.pack(fill=tk.X, pady=(0, 8), after=self.combo_thuat_toan)

    def an_chon_ref(self):
        self.frame_ref_image.pack_forget()

    def cap_nhat_ten_file_ref(self, ten_file):
        self.ten_file_ref_var.set(ten_file)

    def cap_nhat_slider(self, from_, to, resolution, gia_tri_mac_dinh, nhan):
        self.slider.config(from_=from_, to=to, resolution=resolution)
        self.slider_val.set(gia_tri_mac_dinh)
        if nhan == "Gamma":
            self.slider_label_var.set(f"Gamma: {gia_tri_mac_dinh:.1f}")
        elif nhan == "Bit plane":
            self.slider_label_var.set(f"Mặt phẳng bit: {int(gia_tri_mac_dinh)}")
        else:
            self.slider_label_var.set(f"Ngưỡng: {int(gia_tri_mac_dinh)}")

    def cap_nhat_ten_file(self, ten_file):
        self.ten_file_var.set(ten_file)

    def dat_lai_giao_dien(self):
        # Đặt lại nhãn tên file và thuật toán mặc định
        self.ten_file_var.set("Chưa chọn ảnh")
        self.ten_file_ref_var.set("Chưa chọn ảnh tham chiếu")
        self.thuat_toan_var.set("Âm bản")

        # Đặt lại slider đơn (Gamma / Phân ngưỡng) về giá trị khởi tạo
        self.slider_val.set(1.0)
        self.slider_label_var.set("")

        # Đặt lại slider đôi (Contrast Stretching / Gray-level Slicing)
        self.slider_low_val.set(50.0)
        self.slider_high_val.set(200.0)
        self.lbl_low.config(text="50")
        self.lbl_high.config(text="200")

        # Đặt lại checkbox "Giữ nguyên nền"
        self.giu_nen_var.set(False)

        # Ẩn hết slider/checkbox vì thuật toán mặc định (Âm bản) không cần
        self.an_slider()
        self.an_slider_doi()
        self.an_checkbox()
        self.an_chon_ref()
        self.an_giai_thich()

        # Đặt lại khung giải thích về thuật toán mặc định
        self._cap_nhat_giai_thich("Âm bản")

        # Xóa nội dung 4 ô hiển thị, trả về trạng thái ban đầu
        for ax in self.axes.ravel():
            ax.clear()
            ax.axis('off')
            ax.set_facecolor("#dfe6e9")

        self.axes[0, 0].set_title("Original Image",      fontsize=11, fontweight='bold', color="#2c3e50")
        self.axes[0, 1].set_title("Processed Image",     fontsize=11, fontweight='bold', color="#2c3e50")
        self.axes[1, 0].set_title("Original Histogram",  fontsize=11, fontweight='bold', color="#2c3e50")
        self.axes[1, 1].set_title("Processed Histogram", fontsize=11, fontweight='bold', color="#2c3e50")

        self.canvas.draw()

    def lay_thuat_toan(self):
        return self.thuat_toan_var.get()

    def lay_gia_tri_slider(self):
        return self.slider_val.get()

    def lay_gia_tri_slider_doi(self):
        """Trả về (low, high) của slider đôi dưới dạng int."""
        low  = int(self.slider_low_val.get())
        high = int(self.slider_high_val.get())
        if low >= high:
            high = low + 1
        return low, high

    def lay_giu_nen(self):
        """Trả về trạng thái checkbox Giữ nguyên nền."""
        return self.giu_nen_var.get()