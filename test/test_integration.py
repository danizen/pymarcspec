import pytest
from pymarcspec.search import main


@pytest.mark.integration
def test_cli_search(jama_path, capsys):
    main(['marcsearch', '650[0]$0', jama_path])
    out, err = capsys.readouterr()
    assert out == 'https://id.nlm.nih.gov/mesh/D008511\n'


@pytest.mark.integration
def test_cli_search(jama_path, capsys):
    main(['marcsearch', '9.3$b', jama_path])
    out, err = capsys.readouterr()
    assert out == '20190507\n'
