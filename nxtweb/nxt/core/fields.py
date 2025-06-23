from django import forms


class SelectBooleanField(forms.TypedChoiceField):

    def __init__(self, *args, **kwargs):
        valores = {'0': False, '1': True}
        kwargs['coerce'] = lambda x: valores.get(x)
        kwargs['choices'] = (
            ('0', 'NÃO'),
            ('1', 'SIM'),
        )
        super().__init__(*args, **kwargs)


class NullSelectBooleanField(forms.TypedChoiceField):

    def __init__(self, empty_label='TODOS', *args, **kwargs):
        self.empty_label = empty_label
        values = {'0': False, '1': True}
        kwargs['coerce'] = lambda x: values.get(x, '')
        kwargs['choices'] = (
            ('', self.empty_label),
            ('0', 'NÃO'),
            ('1', 'SIM'),
        )
        super().__init__(*args, **kwargs)

