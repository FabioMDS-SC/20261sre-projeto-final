import pytest
from unittest.mock import MagicMock, patch
from scripts.ingestion import get_clickhouse_client, run_ingestion

def test_heartbeat_fail_retries(mocker):
    # Mock do cliente ClickHouse que falha
    mock_client = MagicMock()
    mock_client.command.side_effect = Exception("Connection Failed")
    
    # Mock do clickhouse_connect.get_client para retornar nosso mock_client
    mocker.patch("clickhouse_connect.get_client", return_value=mock_client)
    
    # Como usamos tenacity com 5 attempts, o teste deve falhar após as tentativas
    with pytest.raises(Exception, match="Connection Failed"):
        get_clickhouse_client()
    
    # Verifica se o heartbeat (SELECT 1) foi tentado várias vezes
    assert mock_client.command.call_count == 5

@patch("scripts.ingestion.get_clickhouse_client")
@patch("scripts.ingestion.duckdb.connect")
@patch("os.listdir")
def test_run_ingestion_flow(mock_listdir, mock_duckdb, mock_ch_client, tmp_path):
    # Setup mocks
    mock_listdir.return_value = ["test.csv"]
    mock_client = MagicMock()
    mock_ch_client.return_value = mock_client
    
    # Mock DuckDB Relation
    mock_con = MagicMock()
    mock_duckdb.return_value = mock_con
    mock_rel = MagicMock()
    mock_con.sql.return_value = mock_rel
    
    # Simular um chunk de DataFrame e depois None para sair do loop
    import pandas as pd
    df = pd.DataFrame({"col": [1]})
    mock_rel.fetch_df_chunk.side_effect = [df, None]
    
    # Mock do arquivo
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,name\n1,test")
    
    with patch("os.path.join", return_value=str(csv_file)):
        with patch("os.path.exists", return_value=True):
            run_ingestion()
    
    # Verifica se tentou inserir no ClickHouse
    assert mock_client.insert_df.called
    assert mock_client.insert_df.call_count == 1
