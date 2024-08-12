CREATE TABLE news_websites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique identifier
    name TEXT NOT NULL,                     -- Name of the news website
    url TEXT NOT NULL,                      -- URL of the news website
    category TEXT,                          -- Category (National, Regional, Financial, etc.)
    language TEXT,                          -- Language of the news website
    region TEXT,                            -- Region (Northern India, Southern India, Nationwide, etc.)
    state TEXT,                             -- State (Maharashtra, Tamil Nadu, Delhi, etc.)
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date when the entry was added
);

