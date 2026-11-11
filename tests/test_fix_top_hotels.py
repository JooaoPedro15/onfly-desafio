"""Testes adicionais: ordenação de top_hotels."""

from helpers import run_cli

ROWS = [
    {"reservation_id": "R-1", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "100.00"},
    {"reservation_id": "R-2", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "300.00"},
    {"reservation_id": "R-3", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "100.00"},
]


def test_top_hotels_desc_by_value_with_tie_by_hotel_id_asc(tmp_path):
    """Valor decrescente; empate por hotel_id ascendente (reverse=True quebraria o empate)."""
    report = run_cli(tmp_path, ROWS)
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H03", "H01", "H02"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["300.00", "100.00", "100.00"]


def test_top_cut_respects_tie_break(tmp_path):
    """No corte do --top, o empate decide quem entra: H01 antes de H02."""
    report = run_cli(tmp_path, ROWS, top=2)
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H03", "H01"]
