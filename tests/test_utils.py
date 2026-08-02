from app.utils import format_currency

def test_format_currency_with_decimal():
    input_value = 1234.56
    result = format_currency(input_value)

    assert result == "R$ 1.234,56"

def test_format_currency_with_integer():
    input_value = 1000
    result = format_currency(input_value)

    assert result == "R$ 1.000,00"

def test_format_currency_with_zero():
    input_value = 0
    result = format_currency(input_value)

    assert result == "R$ 0,00"