/* TODO: link with requests */
CREATE TABLE IF NOT EXISTS http_responses(
  site_id INTEGER NOT NULL,
  link_id INTEGER NOT NULL,
  response_id INTEGER NOT NULL,
  url TEXT NOT NULL,
  method TEXT NOT NULL,
  referrer TEXT NOT NULL,
  response_status INTEGER NOT NULL,
  response_status_text TEXT NOT NULL,
  is_cached BOOLEAN NOT NULL,
  headers TEXT NOT NULL,
  location TEXT NOT NULL,
  time_stamp TEXT NOT NULL,
  file_name TEXT,
  FOREIGN KEY (site_id) REFERENCES site_visits(site_id),
  FOREIGN KEY (link_id) REFERENCES site_visits(link_id),
  PRIMARY KEY (site_id, link_id, response_id) 
);
