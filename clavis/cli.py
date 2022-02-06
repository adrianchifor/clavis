import arrpc
import logging
import sys
import secrets as pysecrets
import click
import clavis.db.ops as db
import clavis.rpc.methods as rpc
import clavis.version as v
import clavis.crypto.shamir as shamir
from clavis.errors import ClavisFatalException

logger = logging.getLogger("clavis")


@click.group()
@click.option("--verbose", default=False, is_flag=True, help="Show debug logs")
def cli(verbose):
    """Lightweight, opinionated, paranoid, k8s-native secrets management"""
    if verbose:
        logger.setLevel(logging.DEBUG)


@cli.command()
def version():
    """Show version"""
    click.echo(f"Clavis version {v.version}")


@cli.command()
@click.option("--verbose", default=False, is_flag=True, help="Show debug logs")
@click.option("--gcp-kms", help="GCP KMS key to use for auto unseal")
def server(verbose, gcp_kms):
    """Run keystore server"""
    if verbose:
        logger.setLevel(logging.DEBUG)
    db.patch_psycopg2()
    db.connect()
    click.echo("Running clavis server")

    try:
        rpc.run_server(gcp_kms)
    except ClavisFatalException:
        sys.exit(1)

    # secret = pysecrets.token_hex(64)
    # click.echo(f"secret: {hex(int(secret, base=16))}")
    # shares = shamir.make_random_shares(int(secret, base=16), minimum=3, shares=5)
    # click.echo(f"shares: {shares}")
    # click.echo(f"recovered: {hex(shamir.recover_secret(shares[:3]))}")


@cli.command()
def keystore_init():
    """Initialize Shamir key shares (run on server)"""
    click.echo("Init server keystore")


@cli.command()
def keystore_unseal():
    """Unseal manually with Shamir key shares (run on server)"""
    click.echo("Unsealed server keystore")


@cli.command()
def configure():
    """Configure CLI options (server URL, TLS cert, integrity key)"""
    click.echo("Configuring CLI")


@cli.group()
def secrets():
    """Interact with server keystore as a client"""
    pass


@secrets.command()
def create():
    """Create a secret"""
    click.echo("Created secret")


@secrets.command()
def delete():
    """Delete a secret"""
    click.echo("Deleted secret")


@secrets.command()
def list():
    """List secrets"""
    click.echo("Listed secrets")


@secrets.command()
def read():
    """Read a secret (for k8s service accounts, not users)"""
    click.echo("Reading secret")


@secrets.command()
def update():
    """Update a secret"""
    click.echo("Updated secret")
