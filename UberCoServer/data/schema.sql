CREATE TABLE card (
  id    INTEGER NOT NULL PRIMARY KEY,
  type  INTEGER,
  valid INTEGER
);

CREATE TABLE item (
  id          INTEGER NOT NULL PRIMARY KEY,
  name        TEXT,
  description TEXT,
  is_chest    INTEGER,
  rarity      INTEGER,
  image       TEXT
);

CREATE TABLE reward (
  id              INTEGER NOT NULL PRIMARY KEY,
  name            TEXT,
  description     TEXT,
  rarity          INTEGER,
  numberRemaining INTEGER
);

CREATE TABLE team (
  id     INTEGER NOT NULL PRIMARY KEY,
  name   TEXT,
  colour TEXT
);

CREATE TABLE team_items (
  team_id INTEGER,
  item_id INTEGER
);

CREATE TABLE team_rewards (
  team_id   INTEGER,
  reward_id INTEGER
);

CREATE TABLE chest_keys (
  chest_id INTEGER,
  key_id   INTEGER
);