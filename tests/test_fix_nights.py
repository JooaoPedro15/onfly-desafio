"""Testes adicionais: cálculo de noites de quarto."""

from datetime import date

import pytest
from helpers import run_cli

from onfly_report.services.stay_calculator import calculate_room_nights


@pytest.mark.parametrize(
    "checkin, checkout, rooms, expected",
    [
        pytest.param(date(2024, 12, 30), date(2025, 1, 2), 1, 3, id="virada-de-ano"),
        pytest.param(date(2025, 1, 10), date(2025, 2, 15), 1, 36, id="cruza-mes-dia-maior"),
        pytest.param(date(2025, 1, 30), date(2025, 2, 2), 2, 6, id="virada-de-mes-dois-quartos"),
        pytest.param(date(2024, 2, 28), date(2024, 3, 1), 1, 2, id="ano-bissexto"),
    ],
)
def test_room_nights_use_full_date_difference(checkin, checkout, rooms, expected):
    """(checkout - checkin).days * rooms, não a diferença do dia do mês."""
    assert calculate_room_nights(checkin, checkout, rooms) == expected


def test_year_boundary_stay_counts_in_checkin_month(tmp_path):
    """Virada de ano: 3 noites, todas no mês do check-in."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2024-12-30",
                "checkout_date": "2025-01-02",
                "amount": "300.00",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 3
    assert report["summary"]["average_nightly_rate_brl"] == "100.00"
    assert report["by_month"] == [
        {"month": "2024-12", "reservations": 1, "room_nights": 3, "total_brl": "300.00"}
    ]
