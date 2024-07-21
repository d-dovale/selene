import pytest

from selene import browser, have
from selene.support._pom import Element, All


class MUIBasicSelect:
    label = Element('label')
    selected_text = Element('.MuiSelect-select')
    input = Element('input')
    items = All('[role=option]').within_browser

    def __init__(self, context, browser):  # noqa
        self.browser = browser
        self.context = context

    @staticmethod
    def by_id(value):
        return MUIBasicSelect(
            browser.element(f'#{value}').element(
                './ancestor::*[contains(concat(" ", normalize-space(@class), " "), " '
                'MuiFormControl-root'
                ' ")]'
            ),
            browser,
        )

    def open(self):
        self.context.click()
        return self

    def choose(self, text):
        self.items.element_by(have.exact_text(text)).click()
        return self

    def select(self, text):
        self.open().choose(text)


@pytest.mark.parametrize(
    'age',
    [
        MUIBasicSelect(browser.element('#BasicSelect+* .MuiFormControl-root'), browser),
        MUIBasicSelect.by_id('demo-simple-select'),
    ],
)
def test_material_ui__react_select__basic_select(age):
    browser.driver.refresh()

    # WHEN
    browser.open('https://mui.com/material-ui/react-select/#basic-select')

    # THEN
    age.label.should(have.exact_text('Age'))
    age.selected_text.should(have.exact_text(''))
    age.input.should(have.value(''))

    # WHEN
    age.select('Twenty')

    # THEN
    age.selected_text.should(have.exact_text('Twenty'))
    age.input.should(have.value('20'))
