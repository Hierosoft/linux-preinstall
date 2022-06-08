See <https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=deb_local>

Until a PyTorch release for CUDA 11.7, CUDA 11.3 and therefore Ubuntu 20.04 Focal Fossa or Fedora 33 is necessary. See setup scripts for details on the arduous apt problems that occur.

The lists of tools in this document are limited to ones I know about and that also have training data readily available and ready to train or have pretrained models.

## AI Tools that use the CUDA Toolkit
### 2D to 3D
- nvdiffrec: a 2D to 3D converter that understands light and therefore works with fewer images
  - The training data download instructions are included.

#### Not recommended
- NVlabs/instant-ngp (Instant NeRFs)
  - Until how to train is made clear, it seems difficult to get started. The fox example seems to be the only example that works, and it has metadata regarding camera positions already. Trying to run commands in the readme results in missing file errors.
