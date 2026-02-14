import pathlib
for p in pathlib.Path('.').rglob('*facebook_conversions_config*'):
    print(p)
