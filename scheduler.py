import threading
import time

import schedule

from crawler import crawl_all_sources, crawl_pending_articles


class CronScheduler:
    def __init__(self):
        self.thread = None
        self.stop_event = threading.Event()
        self.running = False

    def _fetch_links_job(self):
        print("[CRON] Bắt đầu lấy danh sách link...")
        crawl_all_sources()
        print("[CRON] Hoàn thành lấy danh sách link.")

    def _fetch_content_job(self):
        print("[CRON] Bắt đầu cập nhật nội dung chi tiết...")
        crawl_pending_articles()
        print("[CRON] Hoàn thành cập nhật nội dung.")

    def _run_loop(self):
        while not self.stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        if self.running:
            print("Cronjob đã đang chạy.")
            return
        schedule.clear()
        schedule.every().day.at("08:00").do(self._fetch_links_job)
        schedule.every(30).minutes.do(self._fetch_content_job)
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        self.running = True
        print("Cronjob đã bật. Lịch: 08:00 lấy link, mỗi 30 phút cập nhật nội dung.")

    def stop(self):
        if not self.running:
            print("Cronjob hiện không chạy.")
            return
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=5)
        schedule.clear()
        self.running = False
        print("Cronjob đã tắt.")

    def run_manual(self):
        print("Chạy thủ công: lấy link và cập nhật nội dung.")
        self._fetch_links_job()
        self._fetch_content_job()
