import asyncio
import uuid

from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from werkzeug.utils import secure_filename

from yacut import app
from yacut.file_services import upload_file
from yacut.forms import FileForm, URLForm
from yacut.models import URLMap
from yacut.utils import create_url_map
from yacut.constants import DUPLICATE_ERROR, RESERVED_SHORT_ID


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data

        if custom_id and (
            custom_id == RESERVED_SHORT_ID
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            flash(DUPLICATE_ERROR)
            return render_template('index.html', form=form)

        url_map = create_url_map(original, custom_id)

        short_link = url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True
        )

        return render_template(
            'index.html',
            form=form,
            short_link=short_link
        )

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


@app.route('/files', methods=['GET', 'POST'])
def upload_files_view():
    form = FileForm()

    if form.validate_on_submit():
        results = []

        for file in form.files.data:
            filename = secure_filename(file.filename)

            if not filename:
                continue

            disk_filename = f'{uuid.uuid4().hex}_{filename}'

            public_url = asyncio.run(
                upload_file(file.stream, disk_filename)
            )

            url_map = create_url_map(public_url)

            short_link = url_for(
                'redirect_view',
                short_id=url_map.short,
                _external=True
            )

            results.append({
                'filename': filename,
                'short_link': short_link
            })

        return render_template(
            'files.html',
            form=form,
            results=results
        )

    return render_template(
        'files.html',
        form=form,
        results=[]
    )
