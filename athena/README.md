# Query Quilt Package Metadata in AWS Athena

The code in this example shows you to create and query Quilt metadata.

## I. Install Athena CloudFormation templates

There are two Athena templates in this directory.
The first (`athena_cfn`) is only run once, and creates a bucket and workgroup usable by the entire account.
The second (`athena_bucket_cfn`) must be run *once for each Quilt bucket* that should be queryable by Athena.

### A. Per-Account Stack

Note: If you store large amounts of data in multiple regions, you may need to create and manage one workgroup per region rather than one per account.

1. Go to CloudFormation -> Stacks in the AWS Console for the region where most of your buckets are, e.g.: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks
2. Click dropdown "Create stack" -> "With new resources (standard)"
3. Select "Template is ready" (default)
4. Select "Upload a template file" -> "Choose file"
5. Select "athena_cfn.yml" from this repository
6. Click Next
7. Enter "Stack name", e.g.: `your-company-athena-cfn`
8. Enter "Company name", e.g.: `your-company` (for use in an S3 bucket name)
9. Click Next
10. Click Next
11. Review then check "I acknowledge that AWS CloudFormation might create IAM resources"
12. Click "Create change set"
13. Wait until "Status = CREATE_COMPLETE" (may need to refresh using upper-right "cycle" icon)
14. Review Changes
15. Click "Execute" in upper right
16. Select "Roll back all stack resources" (default)
17. Click "Execute change set"


### B. Per-Bucket Stack

From CloudFormation in the same Account and Region as before:

1. Click dropdown "Create stack" -> "With new resources (standard)"
2. Select "Template is ready" (default)
3. Select "Upload a template file" -> "Choose file"
4. Select "athena_bucket_cfn.yml" from this repository
5. Click Next
6. Enter "Stack name", e.g.: `your-bucket-athena-cfn`
7. Enter "QuiltAthenaStack", e.g.: `your-company-athena-cfn` (from part A)
8. Enter "QuiltBucket", e.g.: `your-bucket` (as in 6)
9. Enter "QuiltBucketID", e.g.: `your_bucket` (with '-' replaced by '_')
10. Click Next
11. Click Next
12. At the bottom, open the "Quick-create link" triangle
13. Click "Open quick-create link" to get a wizard that makes it easy to rerun this for multiple buckets
14. Click "Create change set"
15. Wait until "Status = CREATE_COMPLETE" (may need to refresh using upper-right "cycle" icon)
16. Review Changes
17. Click "Execute" in upper right
18. Select "Roll back all stack resources" (default)
19. Click "Execute change set"

### C. Modifications

If you need to edit the cfn files, be sure to lint them before using.

```
$ pip3 install --upgrade taskcat cfn-lint
$ taskcat lint
$ cfn-lint *_cfn.yml
```


## II. Querying Athena Tables in SQL Alchemy

[SQL Alchemy](https://sqlalchemy.org/) is a convenient way to run database queries in Python, including Jupyter notebooks. The [pyathena](https://pypi.org/project/pyathena/) library provides the necessary bindings to connect to Athena from SQL Alchemy.

Be sure the replace `BUCKET` with the name of Quilt bucket that already has CloudFormation tables.

### A. Create the Database Connection

```
BUCKET="your-quilt-bucket-name"
BUCKET_ID=BUCKET.replace("-","_")
import sqlalchemy
from sqlalchemy.engine import create_engine

conn_str = "awsathena+rest://@athena.{region_name}.amazonaws.com:443/"\
           "{schema_name}?s3_staging_dir={s3_staging_dir}"
engine = create_engine(
    conn_str.format(
        region_name="us-east-1",
        schema_name="default",
        s3_staging_dir=quote_plus(f"s3://BUCKET")
    )
)
```

### B. Run a Query that Joins the Views

SQL Alchemy wraps SQL operations in Python objects and lets users create complex SQL queries in Python. The example below executes a join query on the two package metadata views created by the script and returns the result as a Pandas DataFrame.

```
import pandas as pd
from sqlalchemy import column, join, text
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import Table, MetaData

pkgnames_view = Table(
    f"{BUCKET_ID}_quilt_packages_view",
    MetaData(bind=engine),
    autoload=True
)

manifests_view = Table(
    f"{BUCKET_ID}_quilt_objects_view",
    MetaData(bind=engine),
    autoload=True
)

q = select(
        join(
            pkgnames_view,
            manifests_view,
            pkgnames_view.c.hash == manifests_view.c.tophash
        )
    )
df = pd.read_sql(q, engine)
df

```


