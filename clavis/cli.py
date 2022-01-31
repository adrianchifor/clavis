import arrpc
import logging
import secrets as pysecrets
import click
import clavis.db.ops as db
import clavis.version as v
import clavis.crypto.shamir as shamir

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
def server(verbose):
    """Run keystore server"""
    if verbose:
        logger.setLevel(logging.DEBUG)
    db.patch_psycopg2()
    db.connect()
    click.echo('Running clavis server')

    secret = pysecrets.token_hex(64)
    click.echo(f"secret: {hex(int(secret, base=16))}")
    shares = shamir.make_random_shares(int(secret, base=16), minimum=3, shares=5)
    click.echo(f"shares: {shares}")
    click.echo(f"recovered: {hex(shamir.recover_secret(shares[:3]))}")

@cli.command()
def keystore_init():
    """Initialize keystore Shamir key shares (run on server)"""
    click.echo('Init server keystore')

@cli.command()
def configure():
    """Configure CLI options (server URL, TLS cert, integrity key)"""
    click.echo('Configuring CLI')

@cli.group()
def secrets():
    """Interact with server keystore as a client"""
    pass

@secrets.command()
def create():
    """Create a secret"""
    click.echo('Created secret')

@secrets.command()
def delete():
    """Delete a secret"""
    click.echo('Deleted secret')

@secrets.command()
def list():
    """List secrets"""
    click.echo('Listed secrets')

@secrets.command()
def read():
    """Read a secret (for k8s service accounts, not users)"""
    click.echo('Reading secret')

@secrets.command()
def update():
    """Update a secret"""
    click.echo('Updated secret')

# def rpc_handler(request):
#     return ""

# server = arrpc.Server("0.0.0.0", 8443, rpc_handler, metrics=True,
#                       tls_certfile="tls.crt", tls_keyfile="tls.key",
#                       auth_secret="")
# server.start()