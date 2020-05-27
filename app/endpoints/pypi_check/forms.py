# -*- coding: utf-8 -*-
from starlette_wtf import StarletteForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class RequirementsForm(StarletteForm):
    """Lyrics File Upload"""

    requirements = TextAreaField(
        "Requirements",
        validators=[
            DataRequired("Paste requirements.txt here"),
            Length(min=3, max=10000),
        ],
    )
