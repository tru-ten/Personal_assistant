from setuptools import setup, find_namespace_packages

setup(name='triton',
      version='1.0',
      description='Personal assistant to manage notes, contacts and files',
      url='https://github.com/tru-ten/Personal_assistant',
      author='team_6th.py',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      entry_points = {'console_scripts': 'starttriton = triton.triton:main'}
      )