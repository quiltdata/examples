# Query Quilt Package Metadata in AWS Athena

The code in this example 

## Define Tables and Views

The first step is to create tables and views in Athena that point to the package metadata in your bucket. This example includes a script that creates two views that expose the package metadata to AWS Athena.

To run the example on your bucket, run:
`AWS_PROFILE=YOUR_PROFILE python create_package_tables.py <BUCKET>`

The `create_package_tables` script uses boto3 to create two base tables then two views that query those tables and extract additional information into separate columns.

| quilt_named_packages_BUCKET_view | quilt_manifests_BUCKET_view |
| - | - |
| user | tophash |
| name | message |
| timestamp | |
| hash | |

Or, the two views can be joined (on tophash = hash) to produce a complete view of package metadata.

## Querying Athena Tables in SQL Alchemy

[SQL Alchemy](https://sqlalchemy.org/) is a convenient way to run database queries in Python, including Jupyter notebooks. The [pyathena](https://pypi.org/project/pyathena/) library provides the necessary bindings to connect to Athena from SQL Alchemy.

### Create the Database Connection

```
import sqlalchemy
from sqlalchemy.engine import create_engine

from sqlalchemy import create_engine

conn_str = "awsathena+rest://@athena.{region_name}.amazonaws.com:443/"\
           "{schema_name}?s3_staging_dir={s3_staging_dir}"
engine = create_engine(
    conn_str.format(
        region_name="us-east-1",
        schema_name="default",
        s3_staging_dir=quote_plus("s3://BUCKET")
    )
)
```

### Run a Query that Joins the Views

SQL Alchemy wraps SQL operations in Python objects and lets users create complex SQL queries in Python. The example below executes a join query on the two package metadata views created by the script and returns the result as a Pandas DataFrame.

```
import pandas as pd
from sqlalchemy import column, join, text
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import Table, MetaData

pkgnames_view = Table(
    "quilt_named_packages_BUCKET_view",
    MetaData(bind=engine),
    autoload=True
)

manifests_view = Table(
    "quilt_manifests_BUCKET_view",
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


