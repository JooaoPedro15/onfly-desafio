"""Testes adicionais: conversão de câmbio para BRL."""

from decimal import Decimal

from helpers import run_cli

from onfly_report.services.currency_converter import convert_to_brl


def test_convert_multiplies_by_rate_without_rounding():
    """amount * rate_to_brl em Decimal, sem arredondar dentro da conversão."""
    result = convert_to_brl(Decimal("0.75"), "USD", {"USD": Decimal("5.420000")})
    assert isinstance(result, Decimal)
    assert result == Decimal("4.065")


def test_conversion_uses_exact_decimal_before_half_up(tmp_path):
    """0.75 * 5.42 = 4.065 exato -> 4.07; com float seria 4.0649999... -> 4.06."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": "R-1", "currency": "USD", "amount": "0.75"}],
    )
    assert report["summary"]["total_amount_brl"] == "4.07"
