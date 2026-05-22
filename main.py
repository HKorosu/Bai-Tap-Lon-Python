import sys
import textwrap

from db import (
    add_source,
    count_articles,
    delete_source,
    get_categories,
    get_source_by_id,
    get_sources,
    initialize_database,
    list_articles,
    update_source,
)
from scheduler import CronScheduler


def prompt(message):
    try:
        return input(message).strip()
    except KeyboardInterrupt:
        print("\nĐã hủy.")
        return ""


def show_sources():
    sources = get_sources()
    if not sources:
        print("Chưa có nguồn tin nào.")
        return
    print("\nDanh sách nguồn tin:")
    print("ID | Tên nguồn | URL | Danh mục | Ngày tạo")
    for source in sources:
        print(f"{source['id']} | {source['source_name']} | {source['url']} | {source['category_name']} | {source['created_at']}")
    print()


def choose_category():
    categories = get_categories()
    for category in categories:
        print(f"{category['id']}. {category['name']}")
    while True:
        choice = prompt("Chọn category_id: ")
        if not choice:
            return None
        if not choice.isdigit():
            print("Vui lòng nhập số.")
            continue
        choice = int(choice)
        for category in categories:
            if category["id"] == choice:
                return choice
        print("Category không tồn tại.")


def create_source():
    print("\n=== Thêm nguồn tin mới ===")
    name = prompt("Tên nguồn: ")
    if not name:
        print("Tên nguồn không được để trống.")
        return
    url = prompt("URL trang tin: ")
    if not url:
        print("URL không được để trống.")
        return
    category_id = choose_category()
    if category_id is None:
        print("Hủy thao tác thêm.")
        return
    add_source(name, url, category_id)
    print("Đã thêm nguồn tin.")


def edit_source():
    show_sources()
    source_id = prompt("Nhập ID nguồn muốn sửa: ")
    if not source_id.isdigit():
        print("ID không hợp lệ.")
        return
    source = get_source_by_id(int(source_id))
    if not source:
        print("Không tìm thấy nguồn tin.")
        return
    print(f"Sửa nguồn: {source['source_name']} ({source['url']})")
    name = prompt(f"Tên nguồn mới [{source['source_name']}]: ") or source["source_name"]
    url = prompt(f"URL mới [{source['url']}]: ") or source["url"]
    category_id = choose_category()
    if category_id is None:
        category_id = source["category_id"]
    update_source(source["id"], name, url, category_id)
    print("Đã cập nhật nguồn tin.")


def remove_source():
    show_sources()
    source_id = prompt("Nhập ID nguồn muốn xóa: ")
    if not source_id.isdigit():
        print("ID không hợp lệ.")
        return
    confirm = prompt("Bạn có chắc muốn xóa? (y/N): ")
    if confirm.lower() != "y":
        print("Hủy xóa.")
        return
    delete_source(int(source_id))
    print("Đã xóa nguồn tin.")


def manage_sources():
    while True:
        print("\n--- Quản lý nguồn tin ---")
        print("1. Xem danh sách nguồn")
        print("2. Thêm nguồn")
        print("3. Sửa nguồn")
        print("4. Xóa nguồn")
        print("0. Quay lại")
        choice = prompt("Chọn: ")
        if choice == "1":
            show_sources()
        elif choice == "2":
            create_source()
        elif choice == "3":
            edit_source()
        elif choice == "4":
            remove_source()
        elif choice == "0":
            return
        else:
            print("Lựa chọn không hợp lệ.")


def show_articles():
    total = count_articles()
    if total == 0:
        print("Chưa có bài viết nào trong hệ thống.")
        return
    page = 1
    page_size = 10
    while True:
        articles = list_articles(page, page_size)
        if not articles and page > 1:
            print("Không còn trang tiếp theo.")
            page -= 1
            continue
        print(f"\n--- Bài viết (Trang {page}) ---")
        for article in articles:
            status = "Mới" if article["status"] == 0 else "Đã lấy"
            title = textwrap.shorten(article["title"], width=80, placeholder="...")
            print(f"{article['id']:3} | {status:6} | {article['category_name'][:12]:12} | {article['source_name'][:18]:18} | {article['created_at']}\n    {title}\n    {article['url']}")
        print(f"Tổng: {total} bài. Hiển thị {len(articles)} bài.")
        command = prompt("N=Next, P=Prev, Q=Exit: ")
        if not command:
            break
        if command.lower() == "n":
            if page * page_size < total:
                page += 1
            else:
                print("Đây là trang cuối.")
        elif command.lower() == "p":
            if page > 1:
                page -= 1
            else:
                print("Đây là trang đầu.")
        elif command.lower() == "q":
            break
        else:
            print("Lựa chọn không hợp lệ.")


def manage_cron(cron):
    while True:
        print("\n--- Cronjob ---")
        print("1. Bật cronjob")
        print("2. Tắt cronjob")
        print("3. Chạy thủ công ngay")
        print("0. Quay lại")
        choice = prompt("Chọn: ")
        if choice == "1":
            cron.start()
        elif choice == "2":
            cron.stop()
        elif choice == "3":
            cron.run_manual()
        elif choice == "0":
            return
        else:
            print("Lựa chọn không hợp lệ.")


def main():
    try:
        print("Đang khởi tạo database...")
        initialize_database()
        print("✓ Database sẵn sàng.\n")
    except Exception as exc:
        print(f"✗ LỖI: Không thể kết nối database. Kiểm tra MySQL đang chạy và config.py.\n{exc}")
        sys.exit(1)
    
    cron = CronScheduler()
    while True:
        print("\n=== News Aggregator CLI ===")
        print("1. Quản lý nguồn tin")
        print("2. Xem tin tức")
        print("3. Điều khiển Cronjob")
        print("0. Thoát")
        choice = prompt("Chọn: ")
        if choice == "1":
            manage_sources()
        elif choice == "2":
            show_articles()
        elif choice == "3":
            manage_cron(cron)
        elif choice == "0":
            print("Tạm biệt!")
            cron.stop()
            sys.exit(0)
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
