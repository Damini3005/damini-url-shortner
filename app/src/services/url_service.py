import time
import pyshorteners
import logging
from typing import Optional
from src.database.dynamodb_client import DynamoDBClient



# Get a logger instance for this module 
logger = logging.getLogger(__name__)


class UrlService:
  """Encapsulates the business logic for URL shortening"""

  def __init__(self,db_client: DynamoDBClient):
    self.db_client = db_client


  def create_short_url(self, original_url: str, phone_number: str) -> Optional[str]:

    """Generates a short URL using an external service (pyshorteners) and stores the mapping in the database."""
    try:
    #1. Initialize the Shortener
       s = pyshorteners.Shortener()

    # 2.Generate the full short URL from the TinyURL service

       short_url = s.tinyurl.short(str(original_url))
      
       logger.info(f"{short_url} short_url printed")

    # Extract the unique code from the end of the URL 
    # e.g., from 'http://tinyurl.com/2x9d68c2', we get '2x9d68c2'

       short_code = short_url.split('/')[-1]
       logger.info(f"{short_code} short_code printed")

    except Exception as e:
        logger.error(f"Failed to generate short URL using pyshorteners: {e}", exc_info=True)
        return None


    item = {
      "short_code": short_code,
      "original_url": original_url,
      "phone_number": phone_number,
      "created_at": int(time.time()),
     } 
    
    success= self.db_client.create_url_entry(item)
    logger.info(f"{success} success status")
    return short_code if success else None
    
  def get_original_url(self, short_code: str)-> Optional[str]:
     """Retrieves the original URL from a short code."""

     item = self.db_client.get_url_entry_by_short_code(short_code)
     if item:
        return item.get("original_url")
     return None
  
  def delete_short_url(self, short_code: str) -> bool:
     """Deletes a short URL record. Returns True on success, False if not found"""

     item = self.db_client.get_url_entry_by_short_code(short_code)
     if not item:
        logger.warning(f"Delete failed: short code '{short_code}' not found.")
        return False
     
     delete_status = self.db_client.delete_url_entry(short_code)
     return delete_status
       
