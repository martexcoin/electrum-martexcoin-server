from setuptools import setup

setup(
    name="electrum-mxt-server",
    version="1.0",
    scripts=['run_electrum_mxt_server.py','electrum-mxt-server'],
    install_requires=['plyvel','jsonrpclib', 'irc>=11'],
    package_dir={
        'electrummxtserver':'src'
        },
    py_modules=[
        'electrummxtserver.__init__',
        'electrummxtserver.utils',
        'electrummxtserver.storage',
        'electrummxtserver.deserialize',
        'electrummxtserver.networks',
        'electrummxtserver.blockchain_processor',
        'electrummxtserver.server_processor',
        'electrummxtserver.processor',
        'electrummxtserver.version',
        'electrummxtserver.ircthread',
        'electrummxtserver.stratum_tcp',
        'electrummxtserver.stratum_http'
    ],
    description="MarteXcoin Electrum Server",
    author="Thomas Voegtlin",
    author_email="thomasv1@gmx.de",
    license="GNU Affero GPLv3",
    url="https://github.com/martexcoin/electrum-mxt-server/",
    long_description="""Server for the Electrum Lightweight MarteXcoin Wallet"""
)


