# import sys
# import types
# import pandas as pd
# from botocore.client import Config
# import ibm_boto3
#
# def __iter__(self): return 0
#
# # @hidden_cell
# # The following code accesses a file in your IBM Cloud Object Storage. It includes your credentials.
# # You might want to remove those credentials before you share your notebook.
# client_66a35c59e0e44474beb1a026696207e0 = ibm_boto3.client(service_name='s3',
#     ibm_api_key_id='3d8uT7ELZ3kutHBvu8AlghXe1KzVb2xTGaJwaty5dgfp',
#     ibm_auth_endpoint="https://iam.ng.bluemix.net/oidc/token",
#     config=Config(signature_version='oauth'),
#     endpoint_url='https://s3-api.us-geo.objectstorage.service.networklayer.com')
#
# body = client_66a35c59e0e44474beb1a026696207e0.get_object(Bucket='pyconproject-donotdelete-pr-hvlammk95c1rrk',Key='hn_stories.csv')['Body']
# # add missing __iter__ method, so pandas accepts body as file-like object
# if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
#
# df_data_1 = pd.read_csv(body)
# df_data_1.head()
