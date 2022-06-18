import argparse
import sys
import time

import boto3



def create_table_or_view(ddlfile, bucket, pfx, isview=False):
    ath = boto3.client('athena')
    athena_output_path = f's3://{bucket}/.athena/quilt'

    with open(ddlfile) as ddl:
        # Drop the Table if it exists
        if not isview:
            format_str = 'DROP TABLE IF EXISTS `{prefix}_{bucket}`'
            drop_ddl = format_str.format(
                prefix=pfx,
                bucket=bucket
            )
            print(drop_ddl)
            ath.start_query_execution(
                QueryString=drop_ddl,
                ResultConfiguration={'OutputLocation': athena_output_path}
            )
            time.sleep(1)
    
        # Create an external table or view in Athena
        create_ddl = ddl.read().format(
            prefix=pfx,
            bucket=bucket
        )
        print(create_ddl)

        response = ath.start_query_execution(
            QueryString=create_ddl,
            ResultConfiguration={'OutputLocation': athena_output_path}
        )
        time.sleep(2)
        results = ath.get_query_results(
            QueryExecutionId=response['QueryExecutionId']
        )
        print(results)
        

def main(argv):
    parser = argparse.ArgumentParser(description='Create Package Tables and Views in AWS Athena.')
    parser.add_argument("bucket", help='Name of S3 bucket')
    args = parser.parse_args(argv)

    bucket = args.bucket

    manifest_pfx = "quilt_manifests"
    pkgname_pfx = "quilt_named_packages"

    # Create base tables from manifests and pointer files
    create_table_or_view('named_packages.ddl', bucket, pkgname_pfx, isview=False),
    create_table_or_view('manifests.ddl', bucket, manifest_pfx, isview=False)

    
    # Create packages and package-objects views
    create_table_or_view('named_packages_view.ddl', bucket, pkgname_pfx, isview=True)
    create_table_or_view('manifest_objects_view.ddl', bucket, manifest_pfx, isview=True)


if __name__ == "__main__":
    main(sys.argv[1:])
