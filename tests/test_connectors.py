import pytest
from pathlib import Path
from src.connectors.ofx_connector import read_ofx_file

def test_read_ofx_file_returns_structured_data():
    # Resolve o caminho relativo ao arquivo de teste
    test_file_dir = Path(__file__).parent
    file_path_ofx = str(test_file_dir.parent / "NU_FILE.ofx")
    result = read_ofx_file(file_path_ofx)
    assert isinstance(result, dict)
    assert len(result) > 0
    first_transaction = result.get("transactions", [])[0]
    assert "date" in first_transaction
    assert "amount" in first_transaction
    assert "description" in first_transaction
