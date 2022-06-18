CREATE OR REPLACE VIEW "quilt_package_objects_{bucket}_view" AS
WITH
    mv AS (
        SELECT
            regexp_extract("$path", '[^/]+$') as tophash,
            manifest."logical_key",
            manifest."physical_keys",
            manifest."size",
            manifest."hash",
            manifest."meta",
            manifest."user_meta"
        FROM
            "quilt_manifests_{bucket}" as manifest
        WHERE manifest."logical_key" IS NOT NULL
    )
SELECT
    npv."user",
    npv."name",
    npv."timestamp",
    mv."tophash",
    mv."logical_key",
    mv."physical_keys",
    mv."hash",
    mv."meta",
    mv."user_meta"
FROM mv
JOIN
    "quilt_packages_{bucket}_view" as npv
ON
    npv."hash" = mv."tophash"
