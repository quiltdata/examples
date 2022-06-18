CREATE OR REPLACE VIEW "quilt_packages_{bucket}_view" AS
WITH
     npv AS (
         SELECT
                regexp_extract("$path", '^s3:\/\/([^\\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)', 4) as user,
                regexp_extract("$path", '^s3:\/\/([^\\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)\/([^\/]+)', 5) as name,
                regexp_extract("$path", '[^/]+$') as timestamp,
                "quilt_named_packages_{bucket}"."hash"
         FROM "quilt_named_packages_{bucket}"
     ),
     mv AS (
        SELECT
            regexp_extract("$path", '[^/]+$') as tophash,
            manifest."meta",
            manifest."message"
        FROM
            "quilt_manifests_{bucket}" as manifest
        WHERE manifest."logical_key" IS NULL
    )
SELECT
     npv."user",
     npv."name",
     npv."hash",
     npv."timestamp",
     mv."message",
     mv."meta"
FROM npv
JOIN
     mv
ON
     npv."hash" = mv."tophash"
     
