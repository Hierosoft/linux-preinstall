# CUDA
Until a PyTorch release for CUDA 11.7, CUDA 11.3 and therefore Ubuntu 20.04 Focal Fossa or Fedora 33 is necessary¸ or any other OS listed after choosing version 11.3 ([11.3.1](https://developer.nvidia.com/cuda-11-3-1-download-archive?target_os=Linux) should work) at the [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive). See setup scripts for details on the arduous apt problems that occur.


## Install
Installing CUDA will have to be done using the steps at the site above, but will only work for CUDA toolkit versions that also have a corresponding pytorch and minicuda on pypi. See subfolder(s) in this folder for install scripts related to your distro and version.


## AI Tools that use the CUDA Toolkit
The lists of tools in the subsections below are limited to ones I know about that have training data readily available and are ready to train, or that have pre-trained models.

### 2D to 3D
- [nvdiffrec](https://github.com/NVlabs/nvdiffrec) (2022) by NVLabs: a 2D to 3D converter that understands light and therefore works with fewer images.
  - The training data download & training instructions are included in the readme.

### Mixed Use
#### AI Gigapixel, 2D to 3D, NeRF, and Neural Volume
"[ACM Transactions on Graphics (SIGGRAPH 2022)](https://nvlabs.github.io/instant-ngp/)" has code regarding all 4 topics. Neural Volumes converts cloud/other photos to volumetric data.

The code is at [instant-ngp](https://github.com/NVlabs/instant-ngp) (Instant NeRFs) by NVLabs. The subsections below describe the status.

##### NeRF
Until how to train is made clear, it seems difficult to get started. The fox example seems to be the only example that works (only tested successfully on Windows, but may work on Linux--See the [Install](#install) section above), and it has metadata regarding camera positions already. Trying to run commands in the readme results in missing file errors.
- It is still maintained as of June 2022, so it may work now or in a future commit.
