def format_currency(value:float) -> str:
    """
    Formata um valor monetário em reais (R$) com duas casas decimais.

    Args:
        value (float): O valor monetário a ser formatado.

    Returns:
        str: O valor formatado como uma string em reais.
    """
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')