import os

from pathlib import Path

from django.db.models import Model
from django.views import View

from .exceptions_for_mixins import WrongModelSubClassException, \
    NoModuleAttributeException


TEMPLATE_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

</body>
</html>
"""

TEMPLATE_CONTENT_WITH_CONTEXT_OBJECT_NAME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
{context_object_name}
</body>
</html>
"""

TEMPLATES_DIR = '/templates'


class HTMLTemplateAutoCreateMixin(View):
    put_context_object_name_in_template = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_to_create = None
        self.template_content = TEMPLATE_CONTENT

    def dispatch(self, request, *args, **kwargs):
        self._start_create_template_process()
        return super().dispatch(request, *args, **kwargs)

    def _validation_process(self):
        self._check_model_attribute_exist()
        self._check_model_class_is_valid()
        if self.put_context_object_name_in_template:
            self.template_content = \
                TEMPLATE_CONTENT_WITH_CONTEXT_OBJECT_NAME.format(
                    context_object_name="{{ " + self.context_object_name + " }}"
                )

    def _check_model_class_is_valid(self):
        """Проверка модели на валидность"""
        if not issubclass(self.model, Model):
            raise WrongModelSubClassException(
                f'"{self.model.__class__.__name__}" is not "Model" subclass'
            )

    def _check_model_attribute_exist(self):
        """Проверяет на наличае атрибута Model"""
        if not hasattr(self, 'model'):
            raise NoModuleAttributeException(
                f'"model" attribute missing in {self.__class__.__name__}'
            )

    def _start_create_template_process(self):
        """Создает шаблон"""
        self._validation_process()
        templates_dir = Path('/'.join([os.getcwd(), self.get_app_label(),
                                      TEMPLATES_DIR]))
        if not templates_dir.exists():
            os.mkdir(templates_dir)
        else:
            if self.check_template_exist(str(templates_dir), self.template_name):
                pass
            else:
                self._create_template()

    def get_app_label(self):
        """Возвращает метку модели"""
        return self.model._meta.app_label

    def template_full_path(self, template_path: str, template_name: str):
        """Возвращает полный путь до шаблона"""
        self.template_to_create = Path('/'.join([template_path, template_name]))
        return self.template_to_create

    def check_template_exist(self, template_path: str, template_name: str):
        """Проверяет нужно ли создовать шаблон"""
        if self.template_full_path(template_path, template_name).exists():
            return True
        return False

    def _create_template(self):
        """Создает шаблон и записывает в него контент"""
        with open(self.template_to_create, 'w') as t:
            t.write(self.template_content)
            t.close()
