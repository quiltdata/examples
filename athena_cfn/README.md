# Query Quilt Package Metadata in AWS Athena

The code in this example shows you how to enable the "Queries"
tab of the Quilt Catalog for querying Quilt [metadata](https://docs.quiltdata.com/catalog/metadata)
in SQL with [Quilt's Athena Integration](https://docs.quiltdata.com/advanced/athena).

Note: This version assumes you are using the latest Quilt Catalog stack
(after October 31, 2023), which allows Athena to use Quilt.  This document
therefore only focuses on how to allow Quilt to use Athena.

We encourage you to update to the most recent version.
Otherwise, you will need to use the
[legacy instructions](https://github.com/quiltdata/examples/tree/legacy/athena_cfn).

## I. Prologue: Ensure Source=Quilt Roles for Athena users

Quilt stacks ship with two `Source=Custom` roles
(based on manually-set ARNs managed by AWS)
that automatically grant access to all buckets that have been added to Quilt.
At this time those `Source=Custom` Roles are incompatible with policies created
from the Quilt Admin panel (including Athena policies). If you have not already,
before proceeding you must do the following in the Quilt Admin panel:

1. Create a new Quilt Role (`Source=Quilt`), such as "AthenaQuiltAccess"
1. Create a new Quilt Policy (`Source=Quilt`) with access to any
buckets that your Athena tables will read from, and any other buckets
in the Quilt stack that you wish your users to access.
1. Assign that Role to the Quilt Users that need to access Athena

See [Users and Roles](https://docs.quiltdata.com/catalog/admin)
documentation for more details on managing Roles and Policies.

## II. Upload the CloudFormation template to S3

### A. Install `athena-cfn.yml` CloudFormation template

Note: You must import this template into the same account/region as your Quilt stack.
If you store large amounts of data in multiple regions, you may need to
create and manage one such stack per _region_ (rather than per _account_).

1. Go to AWS Console > CloudFormation > Stacks.
1. Click dropdown "Create stack" > "With new resources (standard)"
1. Select "Template is ready" (default)
1. Select "Upload a template file"
1. Click "Choose File" and select `athena-cfn.yml`
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

1. Click the Outputs tab of the stack
1. Copy the "AthenaPolicy" ARN from the "Value" column
1. Go to your original Quilt CloudFormation stack
1. Click "Update" > "Use current template"
1. Scroll down to "Other parameters" > "ManagedUserRoleExtraPolicies"
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

### D. Grant Quilt access to the new results Bucket

As with (B), you will need to:

1. Go to the "Outputs" tab of the installed template
1. Copy the `OutputBucket` value
1. Go back to "Admin Settings" in your Quilt Repository
1. Go to "Buckets" tab and click "+" create a new one
1. Paste the value from (2) into "Name"
1. Add a user-friendly description, e.g. "Athena Query Output"
1. Click "Add"

That's it.  If you are using the latest Quilt stack, you can
go directly into the Queries tab and start querying any
of the buckets associated with your stack.

## NOTE: Validating CloudFormation files

If you need to edit the CloudFormation YAML files in this example,
we recommend that you lint them as follows.  
Be sure to switch to the appropriate environment before installing new modules.

```
$ pip3 install --upgrade taskcat cfn-lint
$ taskcat lint && cfn-lint *cfn.yml
```
