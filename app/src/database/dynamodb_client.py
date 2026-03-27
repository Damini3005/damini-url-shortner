import boto3
from typing import Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


class DynamoDBClient:
  """A client for interacting with the DynamoDB table"""
  def __init__(self, table_name: str):
     self.dynamodb = boto3.resource("dynamodb",region_name="ap-south-1")
     self.table = self.dynamodb.Table(table_name)

     logger.info(f"DynamoDBClient initialized for table: {table_name}")




  def get_url_entry_by_short_code(self,short_code: str) -> Optional[Dict[str, Any]]:
     """Retrieves a URL entry from DynamoDB by its short code."""

     try:
        response = self.table.get_item(Key={"short_code":short_code})
        return response.get("Item")
     except Exception as e:
        logger.error(f"Error getting item from DynamoDB: {e}", exc_info=True)
        return None
     
  def create_url_entry(self, item:Dict[str, Any]) -> bool:

     """Saves a new url entry to DynamoDB""" 

     try: 
        logger.info(f"Item received to put in db:{item} ",)
        self.table.put_item(Item=item)
        return True
     except Exception as e:
        logger.error(f"Error putting item to DynamoDb: {e}", exc_info=True)
        return False
     

  def delete_url_entry(self, short_code: str) -> bool:
     """Delete URL entry from DynamoDB by its short code.""" 

     try:
        self.table.delete_item(Key={"short_code":short_code}) 
        return True
     except Exception as e:
        logger.error(f"Error deleting item '{short_code}' from DynamoDB: {e}", exc_info=True)
        return False  
