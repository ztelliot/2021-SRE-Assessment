#/bin/bash
export  PATH="/home/gaoxiang/miniconda3/bin:"$PATH
source ~/.bashrc

source activate
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda
conda config --set show_channel_urls yes

python -m pip install --upgrade setupTools
python -m pip install --upgrade pip

pip install fastapi[all]
