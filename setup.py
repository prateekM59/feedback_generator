from setuptools import setup, find_packages

setup(name='feedback_generator',
      version='1.7',
      description='Feedback generator for Egencia Hackathon',
      long_description='Aalksnfdhjash',
      keywords='alndlkas',
      url='https://github.com/prateekM59/torrent_helper',
      author='Prateek Mahajan',
      author_email='prateekmahajan59@gmail.com',
      license='MIT',
      entry_points = {
          'console_scripts': [
               'start_feedback=feedback_generator.command_line:start_sentiment_service'
          ],
      },
      packages = find_packages(),
      install_requires=[
      ],
      zip_safe=False) 