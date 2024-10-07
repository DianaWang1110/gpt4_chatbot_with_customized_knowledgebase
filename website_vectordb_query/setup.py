from setuptools import setup


setup(
    name='website_vectordb_query',
    version='1.0',
    packages=['website_vectordb_query'],
    url='https://github.com/PIpeIQ/website_vectordb_query',
    license='',
    author='saigopinath',
    author_email='sai@pipeiq.ai',
    description='website to vector database functions',
    install_requires=['numpy', 'openai', 'pandas', 'selenium', 'setuptools', 'tiktoken', 'tdqm', 'pinecone-client',
                      'undetected-chromedriver'],
    long_description=open('README.md').read(),
)


