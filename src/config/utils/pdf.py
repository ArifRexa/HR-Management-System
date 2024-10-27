import os
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.crypto import get_random_string

from xhtml2pdf import pisa

import config.settings


class PDF:
    __FILE_PATH = config.settings.MEDIA_ROOT
    __FILE_EXTENSION = ".pdf"
    _letter_head = f"{config.settings.STATIC_ROOT}/stationary/letter_head_new.jpg"
    _font = f"{config.settings.STATIC_ROOT}/stationary/bangla/Siyamrupali.ttf"

    def __init__(
        self,
        file_name=get_random_string(length=12),
        context=None,
        template_path=None,
        letter_head=None,
    ):
        if context is None:
            context = {}
        self.file_name = file_name
        self.context = context
        self.template_path = template_path

    def __get_string_from_template(self) -> BytesIO:
        """

        @return:
        """
        self.context["watermark"] = self._letter_head
        self.context["font"] = self._font
        template = get_template(self.template_path)
        html = template.render(self.context)
        result = BytesIO()
        pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        return result

    def render_to_pdf(self, download=config.settings.DOWNLOAD_PDF):
        """

        @param download:
        @return:
        """
        bytecode = self.__get_string_from_template()
        response = HttpResponse(bytecode.getvalue(), content_type="application/pdf")
        if download:
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{self.file_name}.pdf"'
        return response

    def create(self) -> str:
        """

        @return:
        """
        bytecode = self.__get_string_from_template()
        file = open(self.absolute_file_path(), "wb")
        file.write(bytecode.getvalue())
        file.close()
        return self.absolute_file_path()

    def absolute_file_path(self):
        return f"{self.__FILE_PATH}/{self.file_name}{self.__FILE_EXTENSION}"

    def delete(self) -> bool:
        """

        @param file_path:
        @return bool:
        """
        if os.path.exists(self.absolute_file_path()):
            os.remove(self.absolute_file_path())
            return True
        return False
