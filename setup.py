from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="panoramic-video-generator",
    version="0.1.0",
    author="AI6132 Group 19",
    description="Gen AI project for generating 360-degree top-view panoramic videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "scipy>=1.11.0",
        "tqdm>=4.66.0",
        "trimesh>=4.0.0",
        "pyrender>=0.1.45",
        "matplotlib>=3.7.0",
        "moviepy>=1.0.3",
        "imageio>=2.31.0",
        "imageio-ffmpeg>=0.4.9",
        "pyyaml>=6.0",
    ],
)
