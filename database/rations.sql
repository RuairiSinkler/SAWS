PRAGMA foreign_keys = 1;

CREATE TABLE ingredients (
  id INTEGER NOT NULL PRIMARY KEY,
  name STRING NOT NULL,
  weigher INT,
  ordering INT,
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

--INSERT INTO ingredients VALUES (0, "Wheat", 1, 0);
--INSERT INTO ingredients VALUES (1, "Barley", 1, 1);
--INSERT INTO ingredients VALUES (2, "Soya", 2, 0);
--INSERT INTO ingredients VALUES (3, "Limestone", 2, 1);
--INSERT INTO ingredients VALUES (4, "Soya Oil", NULL, NULL);
--INSERT INTO ingredients VALUES (5, "Methionine", NULL, NULL);
--INSERT INTO ingredients VALUES (6, "Arbocell", NULL, NULL);
--INSERT INTO ingredients VALUES (7, "Premix", NULL, NULL);
--
--INSERT INTO rations VALUES (0, "None");
--
--INSERT INTO ration_ingredients VALUES (0, 0, 0);
--INSERT INTO ration_ingredients VALUES (0, 1, 0);
--INSERT INTO ration_ingredients VALUES (0, 2, 0);
--INSERT INTO ration_ingredients VALUES (0, 3, 0);
--INSERT INTO ration_ingredients VALUES (0, 4, 0);
--INSERT INTO ration_ingredients VALUES (0, 5, 0);
--INSERT INTO ration_ingredients VALUES (0, 6, 0);
--INSERT INTO ration_ingredients VALUES (0, 7, 0);
--
--INSERT INTO rations VALUES (1, "Peak Lay");
--
--INSERT INTO ration_ingredients VALUES (1, 0, 560);
--INSERT INTO ration_ingredients VALUES (1, 1, 300);
--INSERT INTO ration_ingredients VALUES (1, 2, 210);
--INSERT INTO ration_ingredients VALUES (1, 3, 320);
--INSERT INTO ration_ingredients VALUES (1, 4, 100);
--INSERT INTO ration_ingredients VALUES (1, 5, 20);
--INSERT INTO ration_ingredients VALUES (1, 6, 6.7);
--INSERT INTO ration_ingredients VALUES (1, 7, 40);


