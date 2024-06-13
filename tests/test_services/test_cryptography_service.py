from src.services.cryptography_service import CryptographyService


class TestCryptographyService:
    def test_get_hashed_password(self):
        crypto_service = CryptographyService()
        password = "secret"
        hashed_password = crypto_service.get_hashed_password(password)
        assert hashed_password != password
        assert hashed_password is not None

    def test_check_password_correct(self):
        crypto_service = CryptographyService()
        password = "secret"
        hashed_password = crypto_service.get_hashed_password(password)
        assert crypto_service.check_password(password, hashed_password)

    def test_check_password_incorrect(self):
        crypto_service = CryptographyService()
        password = "secret"
        wrong_password = "incorrect"
        hashed_password = crypto_service.get_hashed_password(password)
        assert not crypto_service.check_password(wrong_password, hashed_password)
