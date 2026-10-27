from setuptools import setup, find_packages

setup(
    name="llm-multi-agent-analytics",
    version="0.1.0",
    description="LLM-powered multi-agent CSV analytics platform",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
)
