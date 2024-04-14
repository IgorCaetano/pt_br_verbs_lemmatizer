from setuptools import setup


with open(r'README.md','r',encoding='utf-8') as f:
    descricao_longa = f.read()

setup(
    name='pt_br_verbs_lemmatizer',
    version='0.1.7',
    # packages=find_packages(),
    packages=[
        "pt_br_verbs_lemmatizer",
        "pt_br_verbs_lemmatizer.dataset"
    ],
    package_dir={"": "src"},
    package_data={"pt_br_verbs_lemmatizer.dataset": ["*.msgpack"]},
    include_package_data = True,
    install_requires = ['msgpack==1.0.7'],
    description='Program designed to lemmatize the various verbal inflections present in the Brazilian Portuguese language quickly and efficiently.',
    long_description=descricao_longa,
    long_description_content_type="text/markdown",
    author='Igor Caetano de Souza',
    project_urls={
        "GitHub Repository":"https://github.com/IgorCaetano/pt_br_verbs_lemmatizer"
    },
)