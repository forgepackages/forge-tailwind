from forgecore.commands import DjangoClickAliasCommand

from forgetailwind.cli import cli


class Command(DjangoClickAliasCommand):
    click_command = cli
