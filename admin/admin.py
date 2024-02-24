from fastapi import APIRouter
from admin.models import OrganizationAdmin
from admin.utils import create_admin, get_admin

admin_router = APIRouter()


@admin_router.post("/api/admin", response_model=OrganizationAdmin)
def admin_create(data: OrganizationAdmin):
    return create_admin(data)

@admin_router.get("/api/admin/get")
def admin_get():
    return get_admin()
