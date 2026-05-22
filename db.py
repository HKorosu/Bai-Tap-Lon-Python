import mysql.connector
from mysql.connector import errorcode, IntegrityError
from config import DB_CONFIG

CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS categories (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(128) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
    CREATE TABLE IF NOT EXISTS sources (
      id INT AUTO_INCREMENT PRIMARY KEY,
      source_name VARCHAR(255) NOT NULL,
      url VARCHAR(512) NOT NULL,
      category_id INT NOT NULL,
      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    """
    CREATE TABLE IF NOT EXISTS articles (
      id INT AUTO_INCREMENT PRIMARY KEY,
      source_id INT NOT NULL,
      category_id INT NOT NULL,
      title VARCHAR(512) NOT NULL,
      url VARCHAR(512) NOT NULL UNIQUE,
      summary TEXT,
      content MEDIUMTEXT,
      status TINYINT NOT NULL DEFAULT 0,
      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE RESTRICT ON UPDATE CASCADE,
      FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
]

CATEGORY_SEED = [
    "Công nghệ",
    "Kinh doanh",
    "Thể thao",
    "Giải trí",
    "Xã hội",
]

SOURCE_SEED = [
    ("Tuổi Trẻ - Kinh doanh", "https://tuoitre.vn/kinh-doanh.htm", 2),
    ("Thanh Niên - Thể thao", "https://thanhnien.vn/the-thao.html", 3),
]


def get_connection(use_database=True):
    config = DB_CONFIG.copy()
    if not use_database:
        config.pop("database", None)
    return mysql.connector.connect(**config)


def execute_query(query, params=None, use_database=True, fetch=False):
    conn = get_connection(use_database=use_database)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            result = None
        conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()


def initialize_database():
    conn = get_connection(use_database=False)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS `{}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(
                DB_CONFIG["database"]
            )
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    try:
        for statement in CREATE_TABLES_SQL:
            cursor.execute(statement)
        for name in CATEGORY_SEED:
            cursor.execute("INSERT IGNORE INTO categories (name) VALUES (%s)", (name,))
        for source in SOURCE_SEED:
            cursor.execute(
                "INSERT IGNORE INTO sources (source_name, url, category_id) VALUES (%s, %s, %s)",
                source,
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_categories():
    return execute_query("SELECT id, name FROM categories ORDER BY id", fetch=True)


def get_sources():
    return execute_query(
        "SELECT s.id, s.source_name, s.url, s.category_id, c.name AS category_name, s.created_at FROM sources s JOIN categories c ON s.category_id = c.id ORDER BY s.id",
        fetch=True,
    )


def get_source_by_id(source_id):
    results = execute_query(
        "SELECT id, source_name, url, category_id FROM sources WHERE id = %s",
        (source_id,),
        fetch=True,
    )
    return results[0] if results else None


def add_source(source_name, url, category_id):
    execute_query(
        "INSERT INTO sources (source_name, url, category_id) VALUES (%s, %s, %s)",
        (source_name.strip(), url.strip(), category_id),
    )


def update_source(source_id, source_name, url, category_id):
    execute_query(
        "UPDATE sources SET source_name = %s, url = %s, category_id = %s WHERE id = %s",
        (source_name.strip(), url.strip(), category_id, source_id),
    )


def delete_source(source_id):
    execute_query("DELETE FROM sources WHERE id = %s", (source_id,))


def insert_article_link(source_id, category_id, title, url):
    try:
        execute_query(
            "INSERT INTO articles (source_id, category_id, title, url, status) VALUES (%s, %s, %s, %s, 0)",
            (source_id, category_id, title.strip(), url.strip()),
        )
        return True
    except IntegrityError as exc:
        if exc.errno == errorcode.ER_DUP_ENTRY:
            return False
        raise


def get_pending_articles(limit=100):
    return execute_query(
        "SELECT id, url FROM articles WHERE status = 0 ORDER BY created_at LIMIT %s",
        (limit,),
        fetch=True,
    )


def update_article_content(article_id, summary, content):
    execute_query(
        "UPDATE articles SET summary = %s, content = %s, status = 1 WHERE id = %s",
        (summary.strip() if summary else None, content.strip() if content else None, article_id),
    )


def count_articles():
    result = execute_query("SELECT COUNT(*) AS total FROM articles", fetch=True)
    return result[0]["total"] if result else 0


def list_articles(page, page_size=10):
    offset = (page - 1) * page_size
    return execute_query(
        "SELECT a.id, a.title, a.url, a.status, a.created_at, s.source_name, c.name AS category_name "
        "FROM articles a "
        "JOIN sources s ON a.source_id = s.id "
        "JOIN categories c ON a.category_id = c.id "
        "ORDER BY a.created_at DESC LIMIT %s OFFSET %s",
        (page_size, offset),
        fetch=True,
    )
