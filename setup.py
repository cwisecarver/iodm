from setuptools import setup, find_packages

from iodm import __version__


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


requirements = parse_requirements('requirements.txt')

setup(
    name='iodm',
    version=__version__,
    namespace_packages=[
        'iodm',
        'iodm.auth',
        'iodm.schemas',
        'iodm.backends',
        'iodm.auth.providers'
    ],
    packages=find_packages(exclude=("tests*", )),
    package_dir={'iodm': 'iodm'},
    include_package_data=True,
    zip_safe=False,
    provides=[
        'iodm.backends',
        'iodm.auth.providers',
    ],
    entry_points={
        'iodm.schemas': [
            'jsonschema = iodm.schemas.jsonschema:JSONSchema'
        ],
        'iodm.backends': [
            'mongo = iodm.backends.mongo:MongoBackend',
            'ephemeral = iodm.backends.ephemeral:EphemeralBackend',
            'elasticsearch = iodm.backends.elasticsearch:ElasticsearchBackend',
        ],
        'iodm.auth.providers': [
            'osf = iodm.auth.providers.osf:OSFAuthProvider',
            'self = iodm.auth.providers.self:SelfAuthProvider',
            'anon = iodm.auth.providers.anon:AnonAuthProvider',
        ],
    },
)
