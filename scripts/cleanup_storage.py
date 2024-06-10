import logging
import sys
import re
import os

from common.azure_blob_storage import AzureBlobStorageClient

if os.getenv('CONFIRM_TO_RESET') != 'OperateReset':
    sys.exit('Cannot operate reset command.')

logger = logging.getLogger('azure.storage.blob')
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

logger.info('Cleaning up Azure Blob Storage started...')

connection_string = os.getenv('STORAGE_CONNECTION_STRING')
container_prefix = os.getenv('STORAGE_CONTAINER_PREFIX')

logger.info(f'The prefix for containers is: {container_prefix}')

container_names = AzureBlobStorageClient.list_container_names(connection_string)
logger.info(f'{len(container_names)} containers.')

for container_name in container_names:
    logger.info(f'Container = {container_name}')
    if re.match(r'^[a-z0-9-]+$', container_name):
        azure_blob = AzureBlobStorageClient(container_name=container_name)
        container_blobs = list(azure_blob.get_blobs())
        logger.info(f'{len(container_blobs)} blob files.')
        logger.info('\n'.join([f'name = {blob.name}' for blob in container_blobs]))
        azure_blob.container_client.delete_container()
        logger.info('deleted.')
    
    else:
        logger.info('skipping...')
        
logger.info('Cleaning up Azure Blob Storage completed...')
