import attr
import pymarc


class BaseTextStyle:
    def field_text(self, field_or_text):
        return field_or_text

    def subfield_text(self, values):
        return values

    def fields_join(self, results):
        return results


@attr.s(frozen=True)
class TextStyle(BaseTextStyle):
    field_totext = attr.ib(default=True, type=bool)
    join_fields = attr.ib(default=True, type=bool)
    field_delimiter = attr.ib(default='', type=str)
    join_subfields = attr.ib(default=True, type=bool)
    subfield_delimiter = attr.ib(default='', type=str)

    def field_text(self, field_or_text):
        if isinstance(field_or_text, pymarc.Field) and self.field_totext:
            field_or_text = self.field_value(field_or_text)
        return field_or_text

    def field_value(self, field):
        return field.value()

    def subfield_text(self, values):
        if self.join_subfields:
            return self.subfield_delimiter.join(values)
        else:
            return values

    def fields_join(self, results):
        if self.join_fields:
            return self.field_delimiter.join(results)
        else:
            return results
