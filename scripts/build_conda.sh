#/bin/bash

display_end() {
  echo 
  echo "You should close and reopen this terminal and vscode if you are running this within vscode."
  echo 
  echo "Next, if using VS Code, create a vscode workspace (File > Save Workspace As) and set your python"
  echo "interpreter to use '$conda_env_name' as it's environment."
  echo 
  echo "From within vscode you can click ctrl-shift-p and then enter 'python interpreter' and"
  echo "select '$conda_env_name' from the list.  You might be asked to pick a level"
  echo "for the setting to apply but there is no wrong answer."
  echo 
  echo "run \"conda activate $conda_env_name\" to switch into your new or updated environment."
}

check_directory_name() {
  local target_directory="$1"
  if [ "$(basename "$(pwd)")" == "$target_directory" ]; then
    echo "Current directory is '$target_directory'."
    return 0  # Return success (true)
  else
    echo "Current directory is not '$target_directory'."
    return 1  # Return failure (false)
  fi
}

# Example usage:
directory_name="huma-sdk"
check_directory_name "$directory_name"
if [ $? -eq 0 ]; then
  continue
else
  script_dir_name="scripts"
  check_directory_name "$script_dir_name" 
  if [ $? -eq 0 ]; then

    echo "Switching to parent directory to run script."
    cd ..
  else
    echo "Please start this script from the $directory_name directory with './scripts/build_conda.sh'."
    exit 0
  fi
fi


# Check if Miniconda is installed
if ! command -v conda &>/dev/null; then
  echo "Miniconda is not installed. Installing it with Homebrew..."
  
  # Install Miniconda with Homebrew
  brew install --cask miniconda
  
  # Add Miniconda to your PATH (you may need to restart your shell or run 'source ~/.bashrc' or 'source ~/.zshrc' after this)
  echo 'export PATH="/usr/local/Caskroom/miniconda/base/bin:$PATH"' >> ~/.bashrc
  echo 'export PATH="/usr/local/Caskroom/miniconda/base/bin:$PATH"' >> ~/.zshrc
  
  # Inform the user to restart their shell or run 'source ~/.bashrc' or 'source ~/.zshrc'
  echo "Miniconda installed. Please restart your shell or run 'source ~/.bashrc' or 'source ~/.zshrc' to update your PATH."
  echo "Then rerun this script."
else
  echo "Miniconda is already installed."
fi

conda_env_name="huma-sdk"
current_env=$(conda info --env | grep '*' | awk '{print $1}')
if [[ $conda_env_name = $current_env ]] ; then
  echo "Please run 'conda deactivate' and then run this script again."
  # conda deactivate
  exit 0
fi

# Check if the environment exists
if conda env list | grep -q "^$conda_env_name"; then
  echo "Conda environment '$conda_env_name' exists. To continue will delete and rebuild the conda environment."
  read -p "Do you want to continue? (y/n): " choice

  # Check the user's choice
  if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
    echo "Deleting $CONDA_DEFAULT_ENV"
    conda env remove --name "$conda_env_name" -y
    conda create --name $conda_env_name python=3.10 -y
    echo "running install of dependencies in conda environment named $conda_env_name"
    conda run -n $conda_env_name scripts/build_conda_install.sh
  fi
else
  conda create --name $conda_env_name python=3.10 -y
  conda run -n $conda_env_name scripts/build_conda_install.sh
  echo "Activate your huma-sdk environment with \"conda activate $conda_env_name\""
fi
display_end
