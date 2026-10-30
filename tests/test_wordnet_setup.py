import pytest
import wordnet_setup


@pytest.mark.parametrize("download_result", [True, False, "error"])
def test_installer_downloads_only_when_needed_and_verifies(monkeypatch, download_result):
    ready = [False]
    calls = []
    class Corpus:
        def synsets(self, word):
            if not ready[0]:
                raise LookupError("Missing corpus")
            return [word]
    def download(package, **kwargs):
        calls.append(package)
        if download_result == "error":
            raise OSError("Network unavailable")
        ready[0] = download_result
        return download_result
    monkeypatch.setattr(wordnet_setup.nltk.corpus, "wordnet", Corpus())
    monkeypatch.setattr(wordnet_setup.nltk, "download", download)
    monkeypatch.setattr(wordnet_setup.nltk.data, "path", [])
    success, message = wordnet_setup.install_wordnet()
    assert success == (download_result is True)
    assert message
    assert calls == ["wordnet"]
    if success:
        assert wordnet_setup.install_wordnet()[0]
        assert calls == ["wordnet"]
