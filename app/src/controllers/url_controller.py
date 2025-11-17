from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.models import url_models
from src.services.url_service import UrlService
from src.database.dynamodb_client import DynamoDBClient
from src.utils.settings import settings
from fastapi.responses import RedirectResponse
import logging




router = APIRouter(tags=["URL Controller"])
logger = logging.getLogger(__name__)


@router.get("/")
@router.get("/health", status_code=status.HTTP_200_OK
)
def health_check():
   logger.info("Health check endpoint called.")
   return {"status": "ok"}

# db_client = DynamoDBClient(settings.DYNAMODB_TABLE_NAME)

def get_dynamodb_client() -> DynamoDBClient:
   return DynamoDBClient(settings.DYNAMODB_TABLE_NAME)


def get_urlservice(db_client:DynamoDBClient = Depends(get_dynamodb_client)) -> UrlService:
  return UrlService(db_client)



@router.post("/create", response_model= url_models.CreateUrlResponse, status_code=status.HTTP_201_CREATED)
def create_url(request:Request,payload: url_models.CreateUrlRequest, service: UrlService = Depends(get_urlservice)):
   logger.info(f"{payload} receive")
   short_code = service.create_short_url(payload.original_url, payload.phone_number)
   logger.info(f"{short_code} short code recieve")
   if not short_code:
      raise HTTPException(status_code=500, detail="failed to create short url")
   
   base_url = str(request.base_url)
   short_url = f"{base_url}{short_code}"

   logger.info(f"Created new mapping: {short_url} for phone: {payload.phone_number}")
   return url_models.CreateUrlResponse(short_url=short_url)

@router.get("/{short_code}") #short code is placeholder for real short code "/https://double_digit_solutions.com/23498"
def get_short_code(request:Request,short_code:str,service_url: UrlService = Depends(get_urlservice)):
    
   original_url = service_url.get_original_url(short_code)
   
   if not original_url:
      raise HTTPException(status_code = 404, detail="URL not Found")
   return RedirectResponse(url= original_url)
   
@router.get("/fetch/{short_code}")
def fetch_url(request:Request, short_code: str, service: UrlService = Depends(get_urlservice)):
   url_entry = service.get_original_url(short_code)
   logger.info(f" url entry: {url_entry}")

   if not url_entry:
      raise HTTPException(status_code = 404, detail = "URL not found")
   return url_models.FetchUrlResponse(original_url=url_entry)
   # return {"original_url": url_entry}


@router.delete("/delete/{short_code}")
def delete_short_code(short_code: str, service: UrlService = Depends(get_urlservice)):
   delete_url = service.delete_short_url(short_code)
   logger.info(f"{delete_url} printed")

   if not delete_url:
      logger.error("failed to delete short url")
      raise HTTPException(status_code = 404 , detail = "url not found")
   return {"message": "url deleted successfully"}