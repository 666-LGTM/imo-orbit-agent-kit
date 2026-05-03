from setuptools import find_packages, setup


setup(
    name="mimo-orbit-agent-kit",
    version="0.1.0",
    description="Multi-agent proof pack generator for Xiaomi MiMo Orbit builders",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["orbit-agent-kit=orbit_agent_kit.cli:main"]},
)
