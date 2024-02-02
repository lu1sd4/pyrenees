# Sourced with interactive shells only. Not sourced when zsh -c SOMETHING is called.
fpath=(~/.zsh/completion $fpath)

source ~/.zsh/init.zsh
source ~/.zsh/aliases.zsh
source ~/.zsh/vars.zsh
source ~/.zsh/env.zsh
source ~/.zsh/keybindings.zsh

eval "$(starship init zsh)"
