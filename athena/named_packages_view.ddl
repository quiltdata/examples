CREATE VIEW "{prefix}_{bucket}_view" AS SELECT
regexp_extract("$path", '^s3:\\/\\/([^\\/]+\\/)+([^\\/]+\\/)+([^\\/]+)$', 1) as user,
regexp_extract("$path", '^s3:\\/\\/([^\\/]+\\/)+([^\\/]+\\/)+([^\\/]+)$', 2) as name,
regexp_extract("$path", '[^/]+$') as timestamp,
"named_packages_quilt_blog_reefcheck"."hash"
FROM "{prefix}_{bucket}"