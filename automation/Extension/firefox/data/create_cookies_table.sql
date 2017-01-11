CREATE TABLE IF NOT EXISTS javascript_cookies(
    id INTEGER PRIMARY KEY ASC,
    crawl_id INTEGER,
    visit_id INTEGER,
    visit_domain_id INTEGER,
    change TEXT,
    creationTime DATETIME,
    expiry DATETIME,
    is_http_only INTEGER,
    is_session INTEGER,
    last_accessed DATETIME,
    raw_host TEXT,
    expires INTEGER,
    host TEXT,
    is_domain INTEGER,
    is_secure INTEGER,
    name TEXT,
    path TEXT,
    policy INTEGER,
    status INTEGER,
    value TEXT
);
