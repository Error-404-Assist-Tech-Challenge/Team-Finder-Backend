from fastapi import APIRouter, Response, Depends, Cookie, HTTPException
from auth import AuthHandler
from Payments.models import *

from Organizations.utils import *

auth_handler = AuthHandler()
stripe_router = APIRouter(tags=["Stripe"])


@stripe_router.get("/api/payments", response_model=PaymentsInfo)
def get_payments_info(user_id: str = Depends(auth_handler.auth_wrapper)):
    organization, error = get_organization_info(user_id)
    if error:
        raise HTTPException(status_code=401, detail=error)
    else:
        return organization


@stripe_router.put("/api/payments", response_model=PaymentsInfo)
def get_payments_info(organization_data: PaymentsInfo, user_id: str = Depends(auth_handler.auth_wrapper)):
    organization, error = update_organization_payment(organization_data)
    if error:
        raise HTTPException(status_code=401, detail=error)
    else:
        return organization
