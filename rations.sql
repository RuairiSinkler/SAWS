PRAGMA foreign_keys = 1;

CREATE TABLE houses (
  house_id INTEGER NOT NULL PRIMARY KEY,
  house_name TEXT NOT NULL,
  UNIQUE(house_name)
);

CREATE TABLE rations (
  ration_id INTEGER NOT NULL PRIMARY KEY,
  ration_name TEXT NOT NULL,
  wheat INTEGER NOT NULL,
  barley INTEGER NOT NULL,
  soya INTEGER NOT NULL,
  limestone INTEGER NOT NULL,
  soya_oil INTEGER NOT NULL,
  arbocell INTEGER NOT NULL,
  methionine INTEGER NOT NULL,
  premix INTEGER NOT NULL,
  UNIQUE(ration_name)
);

CREATE TABLE house_rations (
  house_id INTEGER NOT NULL REFERENCES houses(house_id),
  ration_id INTEGER NOT NULL REFERENCES rations(ration_id),
  PRIMARY KEY(house_id, ration_id)
);

INSERT INTO houses VALUES (0, "House 1");
INSERT INTO houses VALUES (1, "House 2");
INSERT INTO houses VALUES (2, "House 3");
INSERT INTO houses VALUES (3, "Manor Wood");
