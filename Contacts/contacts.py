from fastapi import APIRouter, Depends, HTTPException
from auth import AuthHandler
from typing import List
from Contacts.models import Contact
from Contacts.utils import get_organization_contacts

auth_handler = AuthHandler()
contacts_router = APIRouter(tags=["Discussions"])


@contacts_router.get("/api/contacts", response_model=List[Contact])
def get_contacts(user_id: str = Depends(auth_handler.auth_wrapper)):
    contacts, error = get_organization_contacts(user_id)
    if error:
        raise HTTPException(status_code=500, detail="Failed to fetch contacts: " + error)
    else:
        return contacts
