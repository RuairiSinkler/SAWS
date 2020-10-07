PRAGMA foreign_keys = 1;

CREATE TABLE weighers (
  id INTEGER NOT NULL PRIMARY KEY,
  weigher_pin INTEGER NOT NULL,
  increment STRING
);

CREATE TABLE ingredients (
  id INTEGER NOT NULL PRIMARY KEY,
  name STRING NOT NULL,
  augar_pin INTEGER,
  weigher_id INTEGER REFERENCES weighers(id),
  ordering INTEGER,
  UNIQUE(name)
);

CREATE TABLE rations (
  id INTEGER NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  UNIQUE(name)
);

CREATE TABLE ration_ingredients (
  ration_id INTEGER NOT NULL REFERENCES rations(id),
  ingredient_id INTEGER NOT NULL REFERENCES ingredients(id),
  amount DECIMAL(6, 2) NOT NULL
);

CREATE TABLE houses (
  id INTEGER NOT NULL PRIMARY KEY,
  name STRING NOT NULL,
  UNIQUE(name)
);
