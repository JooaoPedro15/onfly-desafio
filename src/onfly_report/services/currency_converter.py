"""Conversão de valores para BRL."""

from __future__ import annotations

from decimal import Decimal


def convert_to_brl(amount: Decimal, currency: str, rates: dict[str, Decimal]) -> Decimal:
    """Converte para BRL com amount * rate_to_brl, em Decimal e sem arredondar."""
    return amount * rates[currency]
