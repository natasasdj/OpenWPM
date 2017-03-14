/* This file is sourced during the initialization
 * of the crawler. Make sure everything is CREATE
 * IF NOT EXISTS, otherwise there will be errors
 */

/* Crawler Tables */


CREATE TABLE IF NOT EXISTS site_visits (
    site_id INTEGER NOT NULL,
    link_id INTEGER NOT NULL,
    site_url VARCHAR(500) NOT NULL,
    resp_time_1 REAL,
    resp_time_2 REAL,
    resp_time_3 REAL,
    no_links INTEGER,
    dtg DATETIME DEFAULT (CURRENT_TIMESTAMP),   
    PRIMARY KEY (site_id, link_id)

);


