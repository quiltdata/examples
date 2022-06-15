CREATE VIEW "{prefix}_{bucket}_view" AS SELECT
regexp_extract("$path", '[^/]+$') as tophash,
"{prefix}_{bucket}"."message"
FROM "{prefix}_{bucket}"
WHERE "{prefix}_{bucket}"."logical_key" IS NULL