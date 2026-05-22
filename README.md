# News Aggregator CLI

Ứng dụng Console thu thập tin tức từ các nguồn báo (VnExpress, Tuổi Trẻ...), lưu vào MySQL với quản lý nguồn tin, xem bài viết phân trang, và cronjob tự động hóa.

## 📋 Yêu cầu hệ thống

- **Python 3.8+**
- **MySQL 5.7+** (hoặc MariaDB)
- **pip** (package manager của Python)

## 🚀 Cài đặt & Khởi động

### Bước 1: Cài đặt Python packages
```bash
pip install -r requirements.txt
```

### Bước 2: Cấu hình Database
Mở file `config.py` và điều chỉnh thông tin kết nối MySQL:
```python
DB_CONFIG = {
    "host": "127.0.0.1",      # IP MySQL server (thường là localhost)
    "user": "root",            # Username MySQL
    "password": "",            # Password MySQL (để trống nếu không có)
    "database": "news_management",  # Tên database (sẽ tạo tự động)
    "port": 3306,              # Port MySQL (mặc định 3306)
}
```

### Bước 3: Chạy ứng dụng
```bash
python main.py
```

Lần đầu chạy, hệ thống sẽ:
- ✅ Tạo database `news_management`
- ✅ Tạo 3 bảng: `categories`, `sources`, `articles`
- ✅ Seed 5 danh mục mẫu (Công nghệ, Kinh doanh, Thể thao, Giải trí, Xã hội)
- ✅ Thêm 2 source mẫu (VnExpress, Tuổi Trẻ)

## 📖 Hướng dẫn sử dụng

### Menu chính:
```
=== News Aggregator CLI ===
1. Quản lý nguồn tin
2. Xem tin tức
3. Điều khiển Cronjob
0. Thoát
```

### 1️⃣ Quản lý nguồn tin (Sources)
- **Xem danh sách**: Hiển thị tất cả source đang có
- **Thêm nguồn**: Nhập tên, URL, chọn danh mục
- **Sửa nguồn**: Cập nhật thông tin source
- **Xóa nguồn**: Gỡ bỏ source khỏi hệ thống

### 2️⃣ Xem tin tức (Articles)
- Hiển thị **10 tin/trang** (phân trang)
- Phím tắt:
  - **N**: Trang tiếp theo
  - **P**: Trang trước
  - **Q**: Quay lại menu chính
- Mỗi bài viết hiển thị: ID, trạng thái (Mới/Đã lấy), danh mục, nguồn, ngày lấy

### 3️⃣ Điều khiển Cronjob
**Cronjob 1 - Lấy danh sách link:**
- Chạy lúc **08:00 sáng hàng ngày**
- Tự động quét các URL trong `sources`
- Trích xuất tiêu đề & link bài viết mới
- Lưu vào DB với `status = 0` (chưa lấy nội dung)

**Cronjob 2 - Cập nhật nội dung:**
- Chạy **mỗi 30 phút**
- Tìm bài viết chưa lấy nội dung (`status = 0`)
- Lấy toàn bộ nội dung từ từng link
- Cập nhật DB (`status = 1`)

**Tùy chọn:**
- **1. Bật cronjob**: Kích hoạt lịch trình tự động
- **2. Tắt cronjob**: Dừng lịch trình
- **3. Chạy thủ công ngay**: Test ngay lập tức (không chờ giờ)

## 🗄️ Cấu trúc Database

### Bảng `categories` (Danh mục)
| Trường | Kiểu | Ghi chú |
|-------|------|--------|
| `id` | INT | Khóa chính |
| `name` | VARCHAR(128) | Tên danh mục (Công nghệ, Kinh doanh...) |

### Bảng `sources` (Nguồn tin)
| Trường | Kiểu | Ghi chú |
|-------|------|--------|
| `id` | INT | Khóa chính |
| `source_name` | VARCHAR(255) | Tên nguồn (VnExpress, Tuổi Trẻ...) |
| `url` | VARCHAR(512) | URL trang chính |
| `category_id` | INT | Liên kết đến categories |
| `created_at` | DATETIME | Thời gian tạo |

### Bảng `articles` (Bài viết)
| Trường | Kiểu | Ghi chú |
|-------|------|--------|
| `id` | INT | Khóa chính |
| `source_id` | INT | Liên kết đến sources |
| `category_id` | INT | Liên kết đến categories |
| `title` | VARCHAR(512) | Tiêu đề bài viết |
| `url` | VARCHAR(512) | Link bài viết (UNIQUE) |
| `summary` | TEXT | Tóm tắt (để trống khi lấy link) |
| `content` | MEDIUMTEXT | Nội dung toàn bộ |
| `status` | TINYINT | 0=Chưa lấy nội dung, 1=Đã lấy |
| `created_at` | DATETIME | Thời gian tạo |

## 🔧 Tính năng nổi bật

✅ **Xử lý lỗi mạnh mẽ**
- Bẫy lỗi timeout, network không ổn định
- Bỏ qua website bị chặn, vẫn tiếp tục crawl (không crash)

✅ **Tránh trùng lặp dữ liệu**
- URL có constraint UNIQUE
- Tự động bỏ qua bài viết đã tồn tại

✅ **User-Agent Header**
- Giả lập trình duyệt thật để tránh bị chặn

✅ **Hỗ trợ đa trang báo**
- Tích hợp sẵn VnExpress, Tuổi Trẻ
- Dễ mở rộng cho thêm nguồn khác

## 📺 Video Demo

Link demo đầy đủ:
**[Xem video demo trên Google Drive](https://drive.google.com/your-video-link-here)**

Nội dung video:
- ✅ Khởi động ứng dụng
- ✅ Thêm/Sửa/Xóa source
- ✅ Bật cronjob lấy link
- ✅ Cập nhật nội dung chi tiết
- ✅ Xem bài viết với phân trang
- ✅ Log crawler - hiển thị bài viết được lưu, trùng lặp bị skip

## 📝 Cấu trúc file

```
news_aggregator/
├── main.py              # Entry point - giao diện CLI chính
├── config.py            # Cấu hình database & headers
├── db.py                # Tất cả hàm MySQL (CRUD, query)
├── crawler.py           # Hàm crawl (lấy link, nội dung)
├── scheduler.py         # Cronjob & threading
├── init_db.sql          # Script SQL (reference)
├── requirements.txt     # Danh sách packages cần cài
└── README.md            # File này
```

## 🐛 Troubleshooting

**Q: Lỗi "Unable to connect to MySQL"**
- A: Kiểm tra MySQL đang chạy, kiểm tra username/password trong config.py

**Q: Bài viết mới không xuất hiện**
- A: Bật cronjob hoặc chọn "Chạy thủ công ngay" từ menu Cronjob

**Q: Website bị chặn, crawl không được**
- A: Đó là bảo vệ của website. Hệ thống sẽ bỏ qua và tiếp tục crawl các source khác

## 📧 Liên hệ & Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Python 3.8+ đã cài?
2. MySQL đang chạy?
3. requirements.txt đã cài đầy đủ?

---

**Tạo bởi**: AI Assignment Helper 🤖  
**Ngôn ngữ**: Python 3.8+  
**Database**: MySQL 5.7+

## Cài đặt

1. Kích hoạt XAMPP, bật MySQL.
2. Mở terminal trong thư mục dự án:
   ```powershell
   cd C:\Users\Admin\Documents\news_aggregator
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Khởi tạo database:
   - Mở `phpMyAdmin` hoặc dùng MySQL CLI.
   - Chạy file `init_db.sql` để tạo database và seed categories.

4. Chỉnh cấu hình kết nối MySQL ở `config.py` nếu cần.

## Chạy ứng dụng

```powershell
python main.py
```

## Các tính năng

- Quản lý nguồn tin: Thêm/Sửa/Xóa/Xem nguồn
- Xem bài viết với phân trang Next/Previous
- Bật/Tắt cronjob, chạy thủ công lấy link và cập nhật nội dung
- Tự động kiểm tra trùng URL trước khi lưu

## Ghi chú
- Nếu MySQL dùng mật khẩu khác `root`, cập nhật `config.py`.
- Nếu muốn thêm nguồn mẫu, dùng chức năng `Quản lý nguồn tin`.

## File quan trọng
- `init_db.sql` - tạo DB, bảng, seed category
- `config.py` - cấu hình MySQL
- `db.py` - thao tác MySQL
- `crawler.py` - thu thập link và nội dung
- `scheduler.py` - quản lý cronjob
- `main.py` - giao diện Console
