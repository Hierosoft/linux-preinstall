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
To get to the environment, run:

conda deactivate
conda activate dmodel

or if you are in conda base, try:
activate dmodel

nvdiffrec-specific Notes:
If you don't have a large amount of video memory, you must reduce the 
batch size in each json file as per the readme.

Train:
    python train.py --config configs/bob.json

END


cat >/dev/null <<END
train.py gives an error on GeForce TITAN :( :
/home/owner/miniconda3/envs/dmodel/lib/python3.9/site-packages/torch/cuda/__init__.py:123: UserWarning: 
    Found GPU0 NVIDIA GeForce GTX TITAN which is of cuda capability 3.5.
    PyTorch no longer supports this GPU because it is too old.
    The minimum cuda capability supported by this library is 3.7.
    
  warnings.warn(old_gpu_warn % (d, name, major, minor, min_arch // 10, min_arch % 10))

TITAN and TITAN BLACK both only go up to 3.5 according to
<https://developer.nvidia.com/cuda-gpus>

An error also appears:

/home/redacted/miniconda3/envs/dmodel/lib/python3.9/site-packages/nvdiffrast/common/glutil.h:36:10: fatal error: EGL/egl.h: No such file or directory
   36 | #include <EGL/egl.h>
      |          ^~~~~~~~~~~

Which according to <https://github.com/naelstrof/slop/issues/88> is
solved by:
    sudo apt-get install libegl1-mesa-dev

But the warning remains and is followed by:
Traceback (most recent call last):
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/train.py", line 562, in <module>
    ref_mesh         = mesh.load_mesh(FLAGS.ref_mesh, FLAGS.mtl_override)
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/mesh.py", line 82, in load_mesh
    return obj.load_obj(filename, clear_ks=True, mtl_override=mtl_override)
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/obj.py", line 52, in load_obj
    all_materials += material.load_mtl(os.path.join(obj_path, line.split()[1]), clear_ks) # Read in entire material library
  File "/home/owner/miniconda3/envs/dmodel/lib/python3.9/site-packages/torch/autograd/grad_mode.py", line 27, in decorate_context
    return func(*args, **kwargs)
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/material.py", line 92, in load_mtl
    mat['kd'] = texture.srgb_to_rgb(mat['kd'])
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/texture.py", line 142, in srgb_to_rgb
    return Texture2D(list(util.srgb_to_rgb(mip) for mip in texture.getMips()))
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/texture.py", line 142, in <genexpr>
    return Texture2D(list(util.srgb_to_rgb(mip) for mip in texture.getMips()))
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/util.py", line 53, in srgb_to_rgb
    out = torch.cat((_srgb_to_rgb(f[..., 0:3]), f[..., 3:4]), dim=-1) if f.shape[-1] == 4 else _srgb_to_rgb(f)
  File "/home/owner/Downloads/git/NVlabs/nvdiffrec/render/util.py", line 49, in _srgb_to_rgb
    return torch.where(f <= 0.04045, f / 12.92, torch.pow((torch.clamp(f, 0.04045) + 0.055) / 1.055, 2.4))
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call,so the stacktrace below might be incorrect.
For debugging consider passing CUDA_LAUNCH_BLOCKING=1.
END
