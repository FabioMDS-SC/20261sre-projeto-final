import pytest
import os
from scripts.ingestion import validate_csv

def test_validate_csv_success(tmp_path):
    # Criar um arquivo CSV temporário
    d = tmp_path / "data"
    d.mkdir()
    f = d / "test.csv"
    f.write_text("col1,col2\n1,2")
    
    assert validate_csv(str(f)) is True

def test_validate_csv_not_found():
    with pytest.raises(FileNotFoundError):
        validate_csv("arquivo_inexistente.csv")

def test_validate_csv_empty(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    f = d / "empty.csv"
    f.write_text("")
    
    with pytest.raises(ValueError, match="Arquivo vazio"):
        validate_csv(str(f))
