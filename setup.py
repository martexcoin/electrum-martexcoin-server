from setuptools import setup

setup(
    name="electrum-ltc-server",
    version="1.0",
    scripts=['run_electrum_ltc_server.py','electrum-ltc-server'],
    install_requires=['plyvel','jsonrpclib', 'irc>=11'],
    package_dir={
        'electrumltcserver':'src'
        },
    py_modules=[
        'electrumltcserver.__init__',
        'electrumltcserver.utils',
        'electrumltcserver.storage',
        'electrumltcserver.deserialize',
        'electrumltcserver.networks',
        'electrumltcserver.blockchain_processor',
        'electrumltcserver.server_processor',
        'electrumltcserver.processor',
        'electrumltcserver.version',
        'electrumltcserver.ircthread',
        'electrumltcserver.stratum_tcp',
        'electrumltcserver.stratum_http'
    ],
    description="Litecoin Electrum Server",
    author="Thomas Voegtlin",
    author_email="thomasv1@gmx.de",
    license="GNU Affero GPLv3",
    url="https://github.com/pooler/electrum-ltc-server/",
    long_description="""Server for the Electrum Lightweight Litecoin Wallet"""
)


