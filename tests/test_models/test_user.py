# # import pytest
# # from unittest.mock import patch, MagicMock
# # from src.models.user import User
# # from src.services.validation_service import ValidationService

# # class TestUser:
# #     @pytest.fixture(autouse=True)
# #     def setup_method(self):
# #         self.email = 'test@example.com'
# #         self.password = 'securepassword123'
# #         self.password_hash = 'hashedpassword'
# #         self.cryptography_service = MagicMock()
# #         self.cryptography_service.get_hashed_password.return_value = self.password_hash
# #         self.validation_service = MagicMock()
# #         self.validation_service.is_valid_email_format.return_value = True
# #         self.validation_service.is_valid_password_hash_format.return_value = True

# #     def test_create_user(self):
# #         # with patch('src.services.validation_service', return_value=self.validation_service):

# #         new_user = User.create(self.cryptography_service, self.email, self.password)

# #         assert new_user.email == self.email
# #         assert new_user.password_hash == self.password_hash

# #         self.cryptography_service.get_hashed_password.assert_called_once_with(self.password)

# #             # doit avoir appellé validate_email
# #             # doit avoir appellé validate_password_hash

# #     def test_validate_email(self):
# #         self.user.data_validation_service = self.data_validation_service
# #         self.user.validate_email()
# #         self.data_validation_service.is_valid_email_format.assert_called_once_with(self.email)

# #     def test_validate_email_raises_error_with_invalid_email(self):
# #         self.user.email = 'invalidemail'
# #         self.user.data_validation_service = self.data_validation_service
# #         self.data_validation_service.is_valid_email_format.return_value = False
# #         with pytest.raises(ValueError):
# #             self.user.validate_email()

# #     def test_validate_password_hash(self):
# #         self.user.data_validation_service = self.data_validation_service
# #         self.user.validate_password_hash()
# #         self.data_validation_service.is_valid_password_hash_format.assert_called_once_with(self.password_hash)

# #     def test_validate_password_hash_raises_error_with_invalid_hash(self):
# #         self.user.password_hash = 'invalidhash'
# #         self.user.data_validation_service = self.data_validation_service
# #         self.data_validation_service.is_valid_password_hash_format.return_value = False
# #         with pytest.raises(ValueError):
# #             self.user.validate_password_hash()


# import pytest
# from unittest.mock import AsyncMock, MagicMock, Mock, patch
# from src.models import User

# class TestUser:
#     @pytest.fixture
#     def mocked_validation_service(self):
#         # Créez un mock pour le ValidationService
#         with patch('src.services.ValidationService') as mock:
#             mock.is_valid_email_format.return_value = True
#             yield mock

#     @pytest.fixture
#     def user(self, mocked_validation_service):
#         # Créez une instance de User avec des données de test
#         user = User(email="test@example.com", password_hash="hashed_password")
#         user.validation_service = MagicMock()
#         return user

#     @pytest.fixture
#     def mocked_database_service(self):
#         # Créez un mock pour le DatabaseService
#         with patch('src.services.DatabaseService') as mock:
#             yield mock

#     @pytest.fixture
#     def mocked_cryptography_service(self):
#         # Créez un mock pour le CryptographyService
#         with patch('src.services.CryptographyService') as mock:
#             mock.get_hashed_password.return_value = "hashed_password"
#             yield mock

#     def test_create_user(self, user: User, mocked_cryptography_service: MagicMock):
#         # Testez la création de l'utilisateur avec un mock pour CryptographyService
#         new_user = User.create(email="test@example.com", password="password")
#         assert new_user.email == "test@example.com"
#         assert new_user.password_hash == "hashed_password"
#         assert not new_user.is_active

#     def test_validate_email(self, user: User):
#         # Testez la validation de l'email avec un mock pour ValidationService
#         user.validate_email()
#         # Aucune exception ne doit être levée si l'email est valide

#     def test_validate_password_hash(self, user: User, mocked_validation_service: MagicMock):
#         # Testez la validation du hash du mot de passe avec un mock pour ValidationService
#         mocked_validation_service.is_valid_password_hash_format.return_value = True
#         user.validate_password_hash()
#         # Aucune exception ne doit être levée si le hash du mot de passe est valide
#         # Scénario où le format du hash est invalide
#         mocked_validation_service.is_valid_password_hash_format.return_value = False
#         with pytest.raises(ValueError) as excinfo:
#             user.validate_password_hash()
#         assert "Incorrect password hash format" in str(excinfo.value)  # Vérifiez le message de l'exception

#     # Ajoutez d'autres méthodes de test pour couvrir les différentes fonctionnalités de la classe User
