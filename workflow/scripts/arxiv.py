"""
Create the output tarball for easy arXiv upload.
This script is called from the ``arxiv`` rule.

"""
import subprocess
import shutil
from pathlib import Path
import os
import tarfile


# Params defined in `../rules/arxiv.smk`
verbose = snakemake.params["verbose"]
figexts = snakemake.params["figexts"]
TEMP = snakemake.params["TEMP"]
TEX = snakemake.params["TEX"]
FIGURES = snakemake.params["FIGURES"]
SYWTEXFILE = snakemake.params["SYWTEXFILE"]
TECTONIC = snakemake.params["TECTONIC"]
ZENODO_FILES = snakemake.params["ZENODO_FILES"]
arxiv_tarball_exclude = snakemake.params["arxiv_tarball_exclude"]


# Run tectonic to get the .bbl file
tectonic_args = ["--keep-intermediates"]
if verbose:
    tectonic_args += ["--print"]
else:
    tectonic_args += ["--chatter", "minimal"]
subprocess.check_call([TECTONIC] + tectonic_args + [TEX / "{}.tex".format(SYWTEXFILE)])


# Remove all output except the .bbl and .tex files
for file in TEX.glob(".showyourwork-ms.*"):
    if file.name not in [".showyourwork-ms.bbl", ".showyourwork-ms.tex"]:
        os.remove(file)


# Copy the `tex` folder over to a temporary location
if (TEMP / "arxiv").exists():
    shutil.rmtree(TEMP / "arxiv")
shutil.copytree(TEX, TEMP / "arxiv")


# Rename our temporary files to `ms.*`
for file in (TEMP / "arxiv").glob(".showyourwork-ms.*"):
    os.rename(file, str(file).replace(".showyourwork-ms", "ms"))

# Remove additional unnecessary files
arxiv_tarball_exclude += [
    "**/*.py",
    "**/matplotlibrc",
    "**/.gitignore",
    "**/__pycache__",
    "**/__latexindent_temp.tex",
    "**/sywxml.sty",
    "**/*.zenodo",
]
for name in arxiv_tarball_exclude:
    for file in (TEMP / "arxiv").glob(name):
        try:
            os.remove(file)
        except IsADirectoryError:
            shutil.rmtree(file)

# Remove datasets
for file in ZENODO_FILES:
    if os.path.exists(TEMP / "arxiv" / "figures" / file):
        os.remove(TEMP / "arxiv" / "figures" / file)

# Tar it up
with tarfile.open("arxiv.tar.gz", "w:gz") as tar:
    tar.add(TEMP / "arxiv", arcname="arxiv")
shutil.rmtree(TEMP / "arxiv")
