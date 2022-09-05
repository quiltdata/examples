# Examples of working with Quilt 3 API
See also [docs.quiltdata.com](https://docs.quiltdata.com).

## Athena CloudFormation templates

```
$ pip3 install --upgrade taskcat cfn-lint
$ taskcat lint
$ cfn-lint athena/athena_cfn.yml
```

1. Go to CloudFormation -> Stacks in the AWS Console, e.g.: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks
2. Click dropdown: Create stack -> With new resources (standard)
3. Select "Template is ready" (default)
4. Select "Upload a template file" -> Choose file
5. Select athena/athena_cfn.yml from this repository
6. Click Next
7. Enter Stack name, e.g.: my-company-athena-cfn
8. Enter Company name, e.g.: my-company
9. Click Next
10. Click Next
11. Review then check "I acknowledge that AWS CloudFormation might create IAM resources"
12. Click "Create change set"
13. Wait until Status = CREATE_COMPLETE (may need to refresh using upper-right cycle icon)
14. Review Changes
15. Click Execute in upper right
16. Select "Roll back all stack resources" (default)
17. Click "Execute change set"
