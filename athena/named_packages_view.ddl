CREATE VIEW "{prefix}_{bucket}_view" AS SELECT
"$path" as path,
regexp_extract("$path", '^s3:\/\/([^\\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)', 4) as user,
regexp_extract("$path", '^s3:\/\/([^\\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)', 5) as name,
regexp_extract("$path", '[^/]+$') as timestamp,
"{prefix}_{bucket}"."hash"
FROM "{prefix}_{bucket}"
