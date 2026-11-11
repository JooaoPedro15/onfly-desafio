"""Testes adicionais: política de status faturável."""

from helpers import run_cli

from onfly_report.services.status_policy import is_billable


def test_confirmed_is_billable():
    assert is_billable("CONFIRMED") is True


def test_cancelled_is_not_billable():
    assert is_billable("CANCELLED") is False


def test_no_show_is_not_billable():
    assert is_billable("NO_SHOW") is False


def test_unknown_status_is_not_billable():
    """Só CONFIRMED é faturável; status fora da regra não entra por padrão."""
    assert is_billable("PENDING") is False


def test_non_confirmed_excluded_from_by_month_and_top_hotels(tmp_path):
    """CANCELLED e NO_SHOW não entram em by_month, top_hotels nem na média."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "amount": "100.00"},
            {"reservation_id": "R-2", "status": "NO_SHOW", "amount": "20.00"},
            {
                "reservation_id": "R-3",
                "status": "NO_SHOW",
                "hotel_id": "H02",
                "hotel_name": "Hotel So No Show",
                "checkin_date": "2025-02-10",
                "checkout_date": "2025-02-11",
                "amount": "30.00",
            },
            {
                "reservation_id": "R-4",
                "status": "CANCELLED",
                "hotel_id": "H03",
                "hotel_name": "Hotel So Cancelado",
                "checkin_date": "2025-03-10",
                "checkout_date": "2025-03-11",
                "amount": "40.00",
            },
        ],
    )
    assert report["by_month"] == [
        {"month": "2025-01", "reservations": 1, "room_nights": 1, "total_brl": "100.00"}
    ]
    assert report["top_hotels"] == [
        {"hotel_id": "H01", "hotel_name": "Hotel Teste", "room_nights": 1, "total_brl": "100.00"}
    ]
    assert report["summary"]["average_nightly_rate_brl"] == "100.00"
