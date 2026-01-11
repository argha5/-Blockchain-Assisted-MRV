from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mrv-wrapper",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Blockchain-Assisted MRV for Machine Learning Workloads",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/blockchain-mrv-ml",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "codecarbon>=2.3.0",
        "web3>=6.0.0",
        "psutil>=5.9.0",
        "GPUtil>=1.4.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "api": [
            "flask>=3.0.0",
            "flask-cors>=4.0.0",
            "sqlalchemy>=2.0.0",
        ],
    },
)
