

from fastapi import APIRouter, status, HTTPException, Request, Depends




from app.auth.require_role import require_role

from models import  RoleEnum

#Templates response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["admin"])
templates = Jinja2Templates(directory="templates")

@router.get("/admin/panel", response_class=HTMLResponse)
async def admin_panel(
        request: Request,
        user = Depends(require_role(RoleEnum.ADMIN))
                      ):
    return templates.TemplateResponse("admin_panel/adminPanel.html",
                                      {"request": request, "user": user}
                                      )