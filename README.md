## mediapipe-game
カメラに映った手を認識し、出現するノーツの上で手を握るとノーツが消えスコアが加算される

### 実行
python main.py

必要なパッケージはrequirement.txtに記載(pip install -r requirements.txtでインストール可能)

上記をインストールする際は仮想環境(venv,conda等)で行うことを推奨

#### venvの作成
`仮想環境作成`

python -m venv [newenvname]

`仮想環境を有効化`

Windows:

.\[newenvname]\Scripts\activate

macOS/Linux:

source [newenvname]/bin/activate

`仮想環境を無効化`

deactivate

#### condaの作成(minicondaをインストールしている前提)
`仮想環境を作成`

conda create --name [newenvname] python=[pythonのバージョンを指定]

`仮想環境を有効化`

conda activate [newenvname]

`仮想環境を無効化`

conda deactivate

