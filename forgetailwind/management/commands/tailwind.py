from forgecore.cli import DjangoClickAliasCommand

from forgetailwind.cli import cli


class Command(DjangoClickAliasCommand):
    click_command = cli
