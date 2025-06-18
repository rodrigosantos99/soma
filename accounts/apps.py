from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self) -> None:
        from django.db.models.signals import post_save
        from .models import User
        from .signals import post_save_account_receiver

        # Conecta sinal para criação de estudantes e professores
        post_save.connect(post_save_account_receiver, sender=User)

        # Importa os sinais que escutam post_migrate (executa o código de criação do admin)
        import accounts.signals  # noqa

        return super().ready()
