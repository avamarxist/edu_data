PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS Removals_temp;
CREATE TABLE Removals_temp AS SELECT * FROM Removals;

ALTER TABLE Removals_temp ADD COLUMN var_id INTEGER REFERENCES Variable_Categories(var_id);
UPDATE Removals_temp SET var_id = (
	SELECT var_id FROM Variable_Categories
	WHERE Variable_Categories.var_name = Removals_temp.var_name
		AND Variable_Categories.var_category = Removals_temp.var_category
		AND Variable_Categories.var_type = Removals_temp.var_type
);

DROP TABLE Removals;
CREATE TABLE Removals AS SELECT removal_id, dbn, year, number, discipline_type, var_id FROM Removals_temp
	;
DROP TABLE Removals_temp;

PRAGMA foreign_keys = ON;

SELECT * FROM Removals LIMIT 10000;