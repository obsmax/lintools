import setuptools, os

# fuck distutils2
version_file = os.path.join('lintools', 'version.py')
if not os.path.isfile(version_file):
    raise IOError(version_file)

with open(version_file, "r") as fid:
    for l in fid:
        if l.strip('\n').strip().startswith('__version__'):
            __version__ = l.strip('\n').split('=')[-1].split()[0].strip()
            break
    else:
        raise Exception(f'could not detect __version__ affectation in {version_file}')


with open("Readme.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="lintools", 
    version=__version__,
    author="Maximilien Lehujeur",
    author_email="maximilien.lehujeur@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux"],
    python_requires='>=3.7',
    install_requires=[
        'numpy', 'trash-cli'],
      scripts=[os.path.join('bin', 'psg'),
               os.path.join('bin', 'count'),
               os.path.join('bin', 'dusch'),
               os.path.join('bin', 'iostatbar'),
               os.path.join('bin', 'lll'),
               os.path.join('bin', 'msa'),
               os.path.join('bin', 'psg'),
               os.path.join('bin', 'rdu'),
               os.path.join('bin', 'sigint'),
               os.path.join('bin', 'sigkill'),
               os.path.join('bin', 'sigstop'),
               os.path.join('bin', 'sigcont'),
               os.path.join('bin', 'sigterm'),
               os.path.join('bin', 'sizbytyp'),
               os.path.join('bin', 'taskset.py'),
               os.path.join('bin', 'pdfreduce'),
               os.path.join('bin', 'pdfoptimize'),
               os.path.join('bin', 'mkmov')])
    
    
    
    
    
    
    
    
    

