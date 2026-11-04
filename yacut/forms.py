
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    URL,
)

from yacut.constants import MAX_CUSTOM_ID_LENGTH


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Некорректная ссылка')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=MAX_CUSTOM_ID_LENGTH),
            Regexp(
                r'^[a-zA-Z0-9]+$',
                message='Допустимы только латинские буквы и цифры'
            )
        ]
    )


class FileForm(FlaskForm):
    files = MultipleFileField('Выберите файлы')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        if not any(
            file and file.filename
            for file in self.files.data
        ):
            self.files.errors.append(
                'Выберите хотя бы один файл'
            )
            return False

        return True
