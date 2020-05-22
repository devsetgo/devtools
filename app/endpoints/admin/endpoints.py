# -*- coding: utf-8 -*-
from loguru import logger
from starlette.responses import RedirectResponse
from starlette_wtf import csrf_protect

from app_functions import login_required
from app_functions.email_service import send_user_approved
from app_functions.email_service import send_user_reject
from endpoints.admin import crud as admin_crud
from endpoints.admin import forms
from resources import templates

page_url = "/admin_pages"


@csrf_protect
@login_required.require_login
async def admin_index(request):
    """
    Index page for twitter bots
    """

    approval_list = await admin_crud.get_unreviewed_approvals()

    logger.debug(str(approval_list))
    template = f"{page_url}/admin_open.html"
    context = {
        "request": request,
        "approval_list": approval_list,
    }
    logger.info("page accessed: /admin")
    return templates.TemplateResponse(template, context)


@csrf_protect
@login_required.require_login
async def admin_all_requests(request):
    """
    Index page for twitter bots
    """

    approval_list = await admin_crud.get_all_approvals()

    logger.debug(str(approval_list))
    template = f"{page_url}/admin_all.html"
    context = {
        "request": request,
        "approval_list": approval_list,
    }
    logger.info("page accessed: /admin")
    return templates.TemplateResponse(template, context)


@csrf_protect
@login_required.require_login
async def admin_review(request):

    access_id = request.path_params["page"]
    form = await forms.ApprovalReviewForm.from_formdata(request)
    form_data = await request.form()
    approval_info = await admin_crud.review_user(access_id=access_id)

    user_name = approval_info["username"]
    user_info = await admin_crud.user_data(user_name)
    user_email = user_info["email"]
    if form.validate_on_submit():

        if "is_admin" not in form_data:
            is_admin = False
        else:
            is_admin = True

        if "is_active" not in form_data:
            is_active = False
            is_rejected = True
        else:
            is_active = True
            is_rejected = False

        if is_active == True:

            data = {
                "access_id": access_id,
                "user_name": user_name,
                "is_reviewed": True,
                "is_rejected": is_rejected,
                "is_active": is_active,
                "is_admin": is_admin,
            }

            logger.critical(data)
            await admin_crud.update_user_review(data)
            logger.warning(user_email)
            send_user_approved(user_email)
            logger.info("Redirecting user to index page /admin/open")
            return RedirectResponse(url="/admin/open", status_code=303)

        else:

            data = {
                "access_id": access_id,
                "user_name": user_name,
                "is_reviewed": True,
                "is_rejected": True,
                "is_active": False,
                "is_admin": False,
            }
            # update user_apprvoal
            await admin_crud.update_user_review(data)
            # send rejection email
            logger.warning(user_email)
            send_user_reject(user_email)
            logger.info("Redirecting user to index page /admin/open")
            return RedirectResponse(url="/admin/open", status_code=303)

    html_page = request.path_params["page"]
    template = f"{page_url}/admin_review.html"
    context = {
        "request": request,
        "approval_info": approval_info,
        "user_info": user_info,
        "form": form,
    }
    logger.info(f"page accessed: {template}")
    return templates.TemplateResponse(template, context)
