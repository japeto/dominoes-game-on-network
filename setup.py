from setuptools import setup, find_packages

setup(
    name='rest_dominoes',
    version='1.0.0',
    description='Dominoes game on network',
    url='https://github.com/japeto/dominoes-game-on-network',
    author='',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: GNU License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='rest restful api flask swagger dominoes flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restplus==0.9.2', 'Flask-SQLAlchemy==2.1'],
)
