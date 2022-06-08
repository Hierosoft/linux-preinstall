#!/bin/bash
# conda init
cat <<END
11.7 is not on pypi as of 2022 June so install 11.3
as per the nvdiffrec readme except:
- added conditions
- added error avoidance related to CUDA path
END
activate dmodel
me=$0
if [ $? -ne 0 ]; then
    conda create -n dmodel python=3.9
fi
activate dmodel
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'activate dmodel' failed."; exit $code; fi
conda install -y pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'conda install -y pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch' failed."; exit $code; fi
# ^ Change cudatoolkit= part if version differs from installed version.
#   The readme uses 11.3.
pip install ninja imageio PyOpenGL glfw xatlas gdown
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'pip install ninja imageio PyOpenGL glfw xatlas gdown' failed."; exit $code; fi
pip install git+https://github.com/NVlabs/nvdiffrast/
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'pip install git+https://github.com/NVlabs/nvdiffrast/' failed."; exit $code; fi
pip install --global-option="--no-networks" git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'pip install --global-option=\"--no-networks\" git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch' failed."; exit $code; fi
imageio_download_bin freeimage
code=$?
if [ $code -ne 0 ]; then echo "[$me] Error: 'imageio_download_bin freeimage' failed."; exit $code; fi
cat <<END
To get to the model, run:

conda deactivate
conda activate dmodel

or if you are in conda base, try:
activate dmodel

nvdiffrec-specific Notes:
If you don't have a large amount of video memory, you must reduce the 
batch size in each json file as per the readme.
END
