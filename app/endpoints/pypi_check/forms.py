# -*- coding: utf-8 -*-
from starlette_wtf import StarletteForm
from wtforms import BooleanField
from wtforms import FileField
from wtforms import TextAreaField
from wtforms import TextField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.widgets import FileInput


class RequirementsForm(StarletteForm):
    """Lyrics File Upload"""

    requirements = TextAreaField(
        "Requirements",
        validators=[
            DataRequired("Paste requirements.txt here"),
            Length(min=3, max=10000),
        ],
    )
