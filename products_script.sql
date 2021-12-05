BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "PRODUCTS" (
	"ID"	INTEGER NOT NULL,
	"NAME"	TEXT NOT NULL,
	"PRICE"	REAL NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
INSERT INTO "PRODUCTS" VALUES (8,'laptop asus',7000.0);
INSERT INTO "PRODUCTS" VALUES (10,'ram 16gb',350.0);
INSERT INTO "PRODUCTS" VALUES (11,'ssd 500gb',720.0);
INSERT INTO "PRODUCTS" VALUES (12,'monitor lg',12000.0);
INSERT INTO "PRODUCTS" VALUES (13,'pc asus',15000.0);
INSERT INTO "PRODUCTS" VALUES (14,'webcam logitech',520.0);
COMMIT;