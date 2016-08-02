from setuptools import setup

setup(
    name="electrum-martexcoin-server",
    version="0.9",
    scripts=['run_electrum_martexcoin_server','electrum-martexcoin-server'],
    install_requires=['plyvel','jsonrpclib', 'irc>=11'],
    package_dir={
        'electrummartexcoinserver':'src'
        },
    py_modules=[
        'electrummartexcoinserver.__init__',
        'electrummartexcoinserver.utils',
        'electrummartexcoinserver.storage',
        'electrummartexcoinserver.deserialize',
        'electrummartexcoinserver.networks',
        'electrummartexcoinserver.blockchain_processor',
        'electrummartexcoinserver.server_processor',
        'electrummartexcoinserver.processor',
        'electrummartexcoinserver.version',
        'electrummartexcoinserver.ircthread',
        'electrummartexcoinserver.stratum_tcp',
        'electrummartexcoinserver.stratum_http'
    ],
    description="MarteXcoin Electrum Server",
    author="Thomas Voegtlin & Marciano Valverde",
    author_email="thomasv1@gmx.de/marcianovc@gmai.com",
    license="GNU Affero GPLv3",
    url="https://github.com/martexcoin/electrum-martexcoin-server/",
    long_description="""Server for the Electrum Lightweight MarteXcoin Wallet"""
)


