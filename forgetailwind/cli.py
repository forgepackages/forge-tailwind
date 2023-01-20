import os
import sys

import click
from forgecore import Forge

from .core import Tailwind


@click.group("tailwind")
def cli():
    """Tailwind CSS"""
    pass


@cli.command()
def init():
    """Install Tailwind, create a tailwind.config.js and app/static/src/tailwind.css"""
    forge = Forge()
    tailwind = Tailwind(forge.forge_tmp_dir, django_directory=forge.project_dir)

    tailwind_installed = tailwind.is_installed()

    if not tailwind_installed:
        # Need to do an initial download to run init
        tailwind.download()

    # Config needs to exist first so we can save the version here
    if not tailwind.config_exists():
        click.secho("Creating Tailwind config...", bold=True)
        tailwind.create_config()

    if not tailwind_installed:
        # Mostly need to save the version to config...
        click.secho("Installing Tailwind standalone...", bold=True, nl=False)
        version = tailwind.install()
        click.secho(f"Tailwind {version} installed", fg="green")

    if not tailwind.src_css_exists():
        click.secho("Creating Tailwind source CSS...", bold=True)
        tailwind.create_src_css()


@cli.command()
@click.option("--watch", is_flag=True)
@click.option("--minify", is_flag=True)
def compile(watch, minify):
    """Compile a Tailwind CSS file"""
    forge = Forge()
    tailwind = Tailwind(forge.forge_tmp_dir, django_directory=forge.project_dir)

    if not tailwind.is_installed() or tailwind.needs_update():
        version_to_install = tailwind.get_version_from_config()
        if version_to_install:
            click.secho(
                f"Installing Tailwind standalone {version_to_install}...",
                bold=True,
                nl=False,
            )
            version = tailwind.install(version_to_install)
        else:
            click.secho("Installing Tailwind standalone...", bold=True, nl=False)
            version = tailwind.install()
        click.secho(f"Tailwind {version} installed", fg="green")

    args = []
    args.append("-i")
    print(f"Input: {tailwind.src_css_path}")
    args.append(tailwind.src_css_path)

    args.append("-o")
    print(f"Output: {tailwind.dist_css_path}")
    args.append(tailwind.dist_css_path)

    # These paths should actually work on Windows too
    # https://github.com/mrmlnc/fast-glob#how-to-write-patterns-on-windows
    args.append("--content")
    content = ",".join(
        [
            os.path.relpath(forge.project_dir) + "/**/*.{html,js}",
            sys.exec_prefix + "/lib/python*/site-packages/forge*/**/*.{html,js}",
        ]
    )
    print(f"Content: {content}")
    args.append(content)

    if watch:
        args.append("--watch")

    if minify:
        args.append("--minify")

    tailwind.invoke(*args, cwd=os.path.dirname(forge.project_dir))


@cli.command()
def update():
    """Update the Tailwind CSS version"""
    forge = Forge()
    tailwind = Tailwind(forge.forge_tmp_dir, django_directory=forge.project_dir)
    click.secho("Installing Tailwind standalone...", bold=True, nl=True)
    version = tailwind.install()
    click.secho(f"Tailwind {version} installed", fg="green")


if __name__ == "__main__":
    cli()
