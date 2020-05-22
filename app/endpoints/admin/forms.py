# -*- coding: utf-8 -*-

from starlette_wtf import StarletteForm
from wtforms import BooleanField
from wtforms.validators import EqualTo


class ApprovalReviewForm(StarletteForm):
    """ Approve or Reject User """


    is_active = BooleanField()
    is_admin = BooleanField(
        "Admin",
    )
