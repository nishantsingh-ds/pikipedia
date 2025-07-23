from setuptools import setup, find_packages

setup(
    name="wonderbot",
    version="1.0.0",
    description="AI-powered educational web app for kids using CrewAI agents",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-multipart==0.0.6",
        "crewai==0.126.0",
        "crewai-tools==0.51.1",
        "openai==1.3.7",
        "python-dotenv==1.0.0",
        "Pillow==9.5.0",
        "requests==2.31.0"
    ],
    python_requires=">=3.10,<3.14",
) 