python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
python3 -m build
python3 -m twine check dist/*
python3 -m twine upload --repository testpypi dist/*
