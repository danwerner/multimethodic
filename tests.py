import unittest

from multimethods import MultiMethod, method


class NamespaceTests(unittest.TestCase):
    def test_definition_ns_required(self):
        self.assertRaises(TypeError, MultiMethod, 'definition', lambda value: value)

    def test_decorator_ns_required(self):
        MultiMethod('decorator', lambda value: value, ns='custom')

        try:
            @method(1)
            def decorator(value):
                pass
        except TypeError:
            pass
        else:
            self.fail('method decorator does not require namespace')

    def test_definition(self):
        MultiMethod('definition', lambda value: value, ns='custom')
        assert MultiMethod.instances.get('custom.definition'), "namespace is not 'custom'"

    def test_installed_methods(self):
        MultiMethod('installing', lambda value: value, ns='custom')

        try:
            @method(1, ns='custom')
            def installing(value):
                pass
        except KeyError:
            self.fail('not installing multimethods within namespace')
