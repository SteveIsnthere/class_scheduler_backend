import pip

packages_to_install = ['uvicorn', 'Faker', 'pymongo', 'fastapi', 'pydantic', 'pydantic[email]']

for package in packages_to_install:
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
