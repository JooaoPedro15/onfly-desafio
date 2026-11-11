"""Testes adicionais: leitura do arquivo inteiro, sem limite de linhas."""

import csv

from helpers import BASE, COLUMNS, run_cli

from onfly_report.repositories.csv_reservation_repository import CsvReservationRepository


def test_repository_reads_all_rows_beyond_200(tmp_path):
    """O repositório devolve todas as linhas do arquivo, não só as 200 primeiras."""
    path = tmp_path / "reservas.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows({**BASE, "reservation_id": f"R-{i}"} for i in range(1, 251))

    rows = CsvReservationRepository(path).read()

    assert len(rows) == 250
    assert rows[-1].values["reservation_id"] == "R-250"


def test_rows_after_200_enter_counts_totals_and_ranking(tmp_path):
    """Reservas depois da linha 200 entram nas contagens, nos valores e no ranking."""
    rows = [{"reservation_id": f"R-{i}", "amount": "1.00"} for i in range(1, 201)]
    rows += [
        {"reservation_id": "R-201", "hotel_id": "H02", "hotel_name": "Hotel Depois", "amount": "500.00"},
        {"reservation_id": "R-202", "status": "CANCELLED", "amount": "50.00"},
        {"reservation_id": "R-203", "status": "NO_SHOW", "amount": "20.00"},
    ]

    report = run_cli(tmp_path, rows)

    summary = report["summary"]
    assert summary["total_reservations"] == 203
    assert summary["confirmed_reservations"] == 201
    assert summary["cancelled_reservations"] == 1
    assert summary["no_show_reservations"] == 1
    assert summary["total_amount_brl"] == "700.00"
    assert [(h["hotel_id"], h["total_brl"]) for h in report["top_hotels"]] == [
        ("H02", "500.00"),
        ("H01", "200.00"),
    ]
