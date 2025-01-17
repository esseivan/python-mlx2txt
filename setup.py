import glob
from distutils.core import setup

# get all of the scripts
scripts = glob.glob('bin/*')

setup(
  name='mlx2txt',
  packages=['mlx2txt'],
  version='0.8',
  description='A pure python-based utility to extract text and images '
              'from docx files.',
  author='Ankush Shah',
  author_email='ankush.shah.nitk@gmail.com',
  url='https://github.com/esseivan/python-mlx2txt',
  download_url='https://github.com/esseivan/python-mlx2txt/releases',
  keywords=['python', 'mlx', 'text', 'extract'],
  scripts=scripts,
  classifiers=[],
)
