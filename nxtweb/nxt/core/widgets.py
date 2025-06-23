from django.forms.widgets import Select


class BooleanSelect(Select):

    def __init__(self, attrs=None):
        choices = (
            ("true", 'Sim'),
            ("false", 'Não'),
        )
        super().__init__(attrs, choices)

    def format_value(self, value):
        try:
            return {
                True: "true",
                False: "false",
                "true": "true",
                "false": "false",
            }[value]
        except KeyError:
            return "unknown"

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        return {
            True: True,
            "True": True,
            "False": False,
            False: False,
            "true": True,
            "false": False,
        }.get(value)
