from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ["openpyxl"], 'excludes': []}

base = 'gui'

executables = [
    Executable('CWA_AI_App.py', base=base, target_name = 'CWAAPP')
]

setup(name='CWAAPP',
      version = '1',
      description = '1',
      options = {'build_exe': build_options},
      executables = executables)
