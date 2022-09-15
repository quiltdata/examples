# Query Quilt Package Metadata in AWS Athena

The code in this example shows you to enable (and test) use of the "Queries"
pane of the Web Catalog for querying Quilt metadata for specific S3 bucket.

## Overview

There are two Athena templates in this directory.

1. The first (`athena_cfn`) is only run once, and creates a results bucket and
workgroup usable by the entire account (with appropriate permissions).

2. The second (`athena_bucket_cfn`) must be run *once for each Quilt bucket*
that Athena should query. This creates bucket-specific tables and views which
wrap the underlying Quilt metadata.

### NOTE: Validating CloudFormation files

If you need to edit the CloudFormation files, be sure to lint them before use:

```
$ pip3 install --upgrade taskcat cfn-lint
$ taskcat lint && cfn-lint *_cfn.yml
```

## I. Ensure Source=Quilt Roles for Athena users

The initial Quilt deployment ships with two `Source=Custom` Roles that
automatically grant access to all buckets that have been added to Quilt.
Unfortunately, at this time `Source=Custom` Roles are **not** compatible with accessing
Athena.  Therefore, if you have not already, from the Quilt Admin Settings you
must first:

1. Create an empty `Source=Quilt` Role, e.g. "AthenaQuiltAccess"
1. Create a new `Source=Quilt` Policy with access to relevant S3 Buckets, and attach it to that Role
3. Assign that Role to the Quilt users that will need to access Athena

See the [Users and Roles](https://docs.quiltdata.com/catalog/admin)
documentation for more details about using Admin Settings to create and assign Roles.

## II. Create Athena Workgroup

### A. Install `athena_cfn` CloudFormation template

Note: If you store large amounts of data in multiple regions, you may need to
create and manage one such stack per _region_ (rather than per _account_).

1. Go to CloudFormation -> Stacks in the AWS Console for the region where most
of your buckets are, e.g.:
https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks
2. Click dropdown "Create stack" -> "With new resources (standard)"
3. Select "Template is ready" (default)
4. Select "Upload a template file" -> "Choose file"
5. Select "athena_cfn.yml" from this repository
6. Click Next
7. Enter "Stack name", e.g.: `athena-quilt`
9. Click Next
10. Click Next
11. Review then check "I acknowledge that AWS CloudFormation might create IAM resources"
12. Click "Create change set"
13. Wait until "Status = CREATE_COMPLETE" (may need to refresh using upper-right "cycle" icon)
14. Review Changes
15. Click "Execute" in upper right
16. Select "Roll back all stack resources" (default)
17. Click "Execute change set"

### B. Create and attach the new Quilt Policy

After installing `athena_cfn`, you will need to:

1. Go to the "Outputs" tab of the installed template
2. Copy the `AthenaPolicy` ARN
3. Go back to "Admin Settings" in your Quilt Repository
4. Scroll down to "Policies" and click "+" create a new one
5. Enter the friendly name, e.g. "QuiltAthenaAccess"
6. Check "Manually set ARN instead of configuring per-bucket permissions"
7. Paste in the ARN from step (2)
8. Click "Attach current policy to roles..."
9. Select the Role you created in Section I.
10. Click "Create"

Note that it may take a few minutes for the policy credential cache to update.

### C. Grant Quilt access to the new Bucket

As with (B), you will need to:

1. Go to the "Outputs" tab of the installed template
2. Copy the `OutputBucket` value
3. Go back to "Admin Settings" in your Quilt Repository
4. Go to "Buckets" tab and click "+" create a new one
5. Paste that value into "Name"
6. Add a user-friendly description, e.g. "Athena Query Output"
7. Click "Add"

## III. Enable Athena for Individual Buckets

### A. Get link for athena_bucket_cfn

Go to CloudFormation in the same Account and Region as before:

1. Click dropdown "Create stack" -> "With new resources (standard)"
2. Select "Template is ready" (default)
3. Select "Upload a template file" -> "Choose file"
4. Select "athena_bucket_cfn.yml" from this repository
5. Click Next
6. Enter a new "Stack name", e.g.: `your-bucket-athena-quilt`
7. Enter "QuiltAthenaStack", e.g.: `athena-quilt` (from part A)
8. Enter "QuiltBucket", e.g.: `your-bucket` (as in 6)
9. Enter "QuiltBucketID", e.g.: `your_bucket` (with '-' replaced by '_')
10. Click Next
11. Click Next
12. At the bottom, open the "Quick-create link" triangle
13. Click "**Open quick-create link**" to get a wizard that makes it easy to
rerun this for multiple buckets.

Save this link in a shared space so you and other AWS users can easily index additional Quilt buckets.

### B. Use quick-create link for each bucket you want to index

1. Open the link from (C)
2. Update the stack name and bucket parameters
3. Click "Create change set"
4. Wait until "Status = CREATE_COMPLETE" (may need to refresh using upper-right "cycle" icon)
5. Review Changes
6. Click "Execute" in upper right
7. Select "Roll back all stack resources" (default)
8. Click "Execute change set"

### C. Manually invoke view-creating queries

Unfortunately, CloudFormation does not automatically generate the proper views.
To complete setup, you will need to manually execute two pre-defined queries for each bucket:

1. Login to your Quilt Repository
2. Go to the "Queries" tab
3. Click "Select workgroup" (matches the stack name you chose)
4. Click "Select query"
5. Find the "create..." queries corresponding to this bucket
5. Select "create...quilt_packages_view" and click "Run Query"
6. Select "create...quilt_objects_view" and click "Run Query"

### D. Run Athena Queries

From that same Queries tab and workgroup:

1. Click "Select query"
2. Select "preview...quilt_objects_view" and click "Run Query"
3. Click "Filter and Plot" to see (and try out) configuration options
4. Hover over the down arrow in the lower left of the plot
5. Click the "Export" button that appears
6. Under "Save As" type "<bucket-name>-test"
7. Select Current view "<bucket-name>-test.csv"

The results will be saved on your local machine.

