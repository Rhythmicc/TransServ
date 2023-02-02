from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.3"

setup(
    name="TransServ",
    version=VERSION,
    description="监听粘贴板内容并自动拷贝翻译结果",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="Listening clipboard and translate",
    author="RhythmLian",
    url="https://github.com/Rhythmicc/TransServ",
    license="MIT",
    packages=find_packages(),
    package_data={
        "": ["*"],
        "TransServ": ["audio_source/*"],
    },
    zip_safe=True,
    install_requires=["Qpro", "QuickStart_Rhy"],
    entry_points={
        "console_scripts": [
            "ts = TransServ.main:main",
        ]
    },
)
