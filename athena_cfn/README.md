# Query Quilt Package Metadata in AWS Athena

The code in this example shows you to enable (and test) use of the "Queries"
pane of the Web Catalog for querying Quilt metadata for specific S3 bucket.

### NOTE: Validating CloudFormation files

If for any reason you need to edit the CloudFormation files,
be sure to lint them before using:

```
$ pip3 install --upgrade taskcat cfn-lint
$ taskcat lint && cfn-lint *cfn.yml
```

## I. Prologue: Ensure Source=Quilt Roles for Athena users

The initial Quilt deployment ships with two `Source=Custom` Roles that
automatically grant access to all buckets that have been added to Quilt.
Unfortunately, at this time `Source=Custom` Roles are **not** compatible with accessing
Athena.  Therefore, if you have not already, from the Quilt Admin Settings you
must first:

1. Create an empty `Source=Quilt` Role, e.g. "AthenaQuiltAccess"
1. Create a new `Source=Quilt` Policy with access (usually "Read-write") to relevant S3 Buckets, and attach it to that Role
1. Assign that Role to the Quilt Users that need to access Athena

See the [Users and Roles](https://docs.quiltdata.com/catalog/admin)
documentation for more details about using Admin Settings to create and assign Roles and Policies.

## II. Upload Athena Configuration files to S3

There are two Athena templates in this directory,
which must be uploaded directly to S3
(as they are too large to read directly into CloudFormation)

*  `athena-cfn.yml` is only run once, and creates a results bucket and
workgroup usable by the entire account (with appropriate permissions).

* `athena-bucket-cfn.yml` must be run *once for each Quilt bucket*
that Athena should query. This creates bucket-specific tables and views which
wrap the underlying Quilt metadata.

To install these in S3:

1. Go to Amazon S3 -> Buckets  in the AWS Console for the region where most
of your buckets are, e.g.:
https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1
1. Choose any bucket you can read and write to
1. Create or navigate to an appropriate folder
1. Select Upload -> Add files
1. Select both `athena-cfn.yml` and `athena-bucket-cfn.yml` from this repository
1. Click Upload
1. Command-click on each filename to open it in a new browser window
1. Remember or copy and paste the `https` 'Object URL' for each file

## III. Create Athena Workgroup

### A. Install `athena-cfn.yml` CloudFormation template

Note: If you store large amounts of data in multiple regions, you may need to
create and manage one such stack per _region_ (rather than per _account_).

1. Go to CloudFormation -> Stacks in the AWS Console for the region where most
of your buckets are, e.g.:
https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks
1. Click dropdown "Create stack" -> "With new resources (standard)"
1. Select "Template is ready" (default)
1. Select "Amazon S3 URL" (default)
1. Paste in the `athena-cfn.yml` Object URL from above
1. Click Next
1. Enter "Stack name", e.g.: `athena-quilt`
1. Click Next
1. Click Next
1. Review then check "I acknowledge that AWS CloudFormation might create IAM resources"
1. Click "Create change set"
1. Wait until "Status = CREATE_COMPLETE" (may need to refresh using upper-right "cycle" icon)
1. Review Changes
1. Click "Execute" in upper right
1. Select "Roll back all stack resources" (default)
1. Click "Execute change set"

You need to wait until the `athena-cfn.yml` stack creation completes,
so you can use its Outputs for the following steps.

### B. Extend Quilt's Permission Boundary

1. Go to the "Outputs" tab of the installed template
1. Copy the `AthenaPolicy` ARN from the "Value" column
1. Go to your original Quilt CloudFormation stack
1. Click "Update" -> "Use current template"
1. Scroll down to "Other parameters" -> "ManagedUserRoleExtraPolicies"
1. Paste in that ARN (adding a comma if necessary)
1. Click "Next" and then "Next"
1. Check "I acknowledge that AWS CloudFormation might create IAM resources with custom names."
1. Click "Update Stack"


### C. Create and attach the new Quilt Policy

After the `athena-cfn.yml` stack is created, you will need to:

1. Go to the "Outputs" tab of the installed template
1. Copy the `AthenaPolicy` ARN from the "Value" column
1. Go back to "Admin Settings" in your Quilt Repository
1. Scroll down to "Policies" and click "+" create a new one
1. Enter the friendly name, e.g. "QuiltAthenaAccess"
1. Check "Manually set ARN instead of configuring per-bucket permissions"
1. Paste in the ARN from step (2)
1. Click "Attach current policy to roles..."
1. Select the Role you created in Section I.
1. Click "Create"

Note that it may take a few minutes for the policy credential cache to update.

### D. Grant Quilt access to the new Bucket

As with (B), you will need to:

1. Go to the "Outputs" tab of the installed template
1. Copy the `OutputBucket` value
1. Go back to "Admin Settings" in your Quilt Repository
1. Go to "Buckets" tab and click "+" create a new one
1. Paste the value from (2) into "Name"
1. Add a user-friendly description, e.g. "Athena Query Output"
1. Click "Add"

## IV. Enable Athena for Individual Buckets

Note that this process assumes you have already:
* added the relevant S3 bucket to the Quilt registry
* added that bucket to a Policy for the Role from (I)
* created at least one package in that bucket

### A. Get link for athena-bucket-cfn

Go to CloudFormation in the same Account and Region as before:

1. Click dropdown "Create stack" -> "With new resources (standard)"
1. Select "Template is ready" (default)
1. Select "Amazon S3 URL" (default)
1. Paste in the `athena-bucket-cfn.yml` Object URL from before
1. Click Next
1. Enter a new "Stack name", e.g.: `your-bucket-athena-quilt`
1. Enter "QuiltAthenaStack", e.g.: `athena-quilt` (from part III.A.7)
1. Enter "QuiltBucket" to pull metadata from, e.g.: `your-bucket` (without `s3` or `arn` prefixes)
1. Enter "QuiltBucketID", e.g.: `your_bucket` (with '-' replaced by '_')
1. Click Next
1. Click Next
1. At the bottom, open the "Quick-create link" triangle
1. Click "**Open quick-create link**" to get a wizard that makes it easy to
rerun this for multiple buckets.

Save this link in a shared space so you and other AWS users can easily index additional Quilt buckets.

### B. Use quick-create link for each bucket you want to index

1. Open the link from (A.13)
1. Update the stack name and bucket parameters to match THIS bucket
1. Click "Create change set"
1. Wait until "Status = CREATE_COMPLETE" (may need to refresh using upper-right "cycle" icon)
1. Review Changes
1. Click "Execute" in upper right
1. Select "Roll back all stack resources" (default)
1. Click "Execute change set"

### C. Manually invoke view-creating queries

Unfortunately, CloudFormation does not automatically generate the proper views.
To complete setup, you will need to manually execute two pre-defined queries for each bucket:

1. Login to your Quilt Repository
1. Go to the "Queries" tab
1. Click "Select workgroup" (matches the stack name you chose)
1. Click "Select query"
1. Find the "create..." queries corresponding to this bucket
1. Select "create1...quilt_packages_view" and click "Run Query"
1. Select "create2...quilt_objects_view" and click "Run Query"

### D. Run Athena Queries

From that same Queries tab and workgroup:

1. Click "Select query"
1. Select "preview...quilt_objects_view" and click "Run Query"
1. Click "Filter and Plot" to see (and try out) configuration options
1. Hover over the down arrow in the lower left of the plot
1. Click the "Export" button that appears
1. Under "Save As" type "<bucket-name>-test"
1. Select Current view "<bucket-name>-test.csv"

The results will be saved on your local machine.

