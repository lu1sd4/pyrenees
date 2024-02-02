# Sourced on the start of login shell and after zshrc if interactive

XLA_FLAGS=--xla_gpu_cuda_data_dir=/opt/cuda

[[ "$(tty)" = "/dev/tty1" ]] && ! pgrep -x i3>/dev/null && exec startx
true
