# CUDA
Until a PyTorch release for CUDA 11.7, CUDA 11.3 and therefore Ubuntu 20.04 Focal Fossa or Fedora 33 is necessary¸ or any other OS listed after choosing version 11.3 ([11.3.1](https://developer.nvidia.com/cuda-11-3-1-download-archive?target_os=Linux) should work) at the [CUDA Toolkit Archive](https://developer.nvidia.com/cuda-toolkit-archive). See setup scripts for details on the arduous apt problems that occur.

Here are the official documents used for reference and why they didn't solve the issue:
- [CUDA Compatibility](https://docs.nvidia.com/deploy/cuda-compatibility/index.html) "describes the use of new CUDA toolkit components on systems with older base installations" but doesn't describe Python component compatibility.
- [NVIDIA CUDA Toolkit Release Notes](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html): This page lists the minimum driver version for each CUDA version.
  - However, instead of using this list, as noted in [step1-11.3.sh][ubuntu-20.04/step1-11.3.sh] the version you should get is in the name of the package you chose such as nvidia-driver-465 where 465 is the version in the package filename "cuda-repo-ubuntu2004-11-3-local_11.3.1-465.19.01-1_amd64.deb".


## Install
Installing CUDA will have to be done using the steps at the site above, but will only work for CUDA toolkit versions that also have a corresponding pytorch and minicuda on pypi. See subfolder(s) in this folder for install scripts related to your distro and version.


## AI Tools that use the CUDA Toolkit
The lists of tools in the subsections below are limited to ones I know about that have training data readily available and are ready to train, or that have pre-trained models.

### 2D to 3D
- [nvdiffrec](https://github.com/NVlabs/nvdiffrec) (2022) by NVLabs: a 2D to 3D converter that understands light and therefore works with fewer images.
  - The training data download & training instructions are included in the readme.

### Mixed Use
#### AI upscaling and 2D to 3D
Specifically, the techniques in "[ACM Transactions on Graphics (SIGGRAPH 2022)](https://nvlabs.github.io/instant-ngp/)" (2022) are "Neural gigapixel images", "Neural SDF" (non-textured 2D to 3D), NeRF (textured 2D to 3D), and "Neural volumes" (converts cloud/other photos to volumetric data).

The code is at [instant-ngp](https://github.com/NVlabs/instant-ngp) (Instant NeRFs) by NVLabs. The subsections below describe the status.

##### NeRF
Until how to train is made clear, it seems difficult to get started. The fox example seems to be the only example that works (only tested successfully on Windows, but may work on Linux--It failed on a GeForce Titan Black on Windows. See the [Install](#install) section above). The fox example has metadata regarding camera positions already, so whether reproducing the result without that data is possible is unclear. Trying to run commands in the readme results in missing file errors.
- It is still maintained as of June 2022, so it may work now or in a future commit.
