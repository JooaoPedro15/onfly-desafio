"""Testes adicionais: política de status faturável."""

from onfly_report.services.status_policy import is_billable


def test_confirmed_is_billable():
    assert is_billable("CONFIRMED") is True


def test_cancelled_is_not_billable():
    assert is_billable("CANCELLED") is False


def test_no_show_is_not_billable():
    assert is_billable("NO_SHOW") is False