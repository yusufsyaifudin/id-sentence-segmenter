
from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name='id-sentence-segmenter',
        version='0.0.1',
        author='Yusuf Syaifudin',
        author_email='yusuf.syaifudin@gmail.com',
        description="A distributed unique ID generator inspired by Twitter's Snowflake.",
        url="https://github.com/yusufsyaifudin/id-sentence-segmenter",
        packages=find_packages(),
        package_data={"idsentsegmenter": ["*"]},
        include_package_data=True,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Natural Language Processing :: Indonesian Language",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3 :: Only",
        ],
        python_requires=">=3.6",
        project_urls={
            "Documentation": "https://github.com/yusufsyaifudin/id-sentence-segmenter",
        },
        tests_require=(),
    )
