# homecoming-calculator

このプロジェクトは、都市間の移動コスト・時間・交通手段を入力し、出発地から目的地までの最適な経路（コスト＋時間換算）を計算・可視化するWebアプリケーションです。  
NetworkX・Pandas・Streamlitを利用しています。

## 主な機能

- CSVファイルから経路データ（始点・終点・コスト・時間・手段）を読み込み
- StreamlitによるGUIで経路データの編集・保存
- 出発地・目的地・時給（時間の価値）を指定して最適経路を計算
- 経路ごとの合計コスト・合計時間・合計価値（コスト＋時間換算）を表示

## セットアップ

1. Python 3.12 以上をインストールしてください。
2. 必要なパッケージをインストールします。

```bash
pip install .
# または
pip install -r requirements.txt
```

## 使い方

1. `src/main.py` をStreamlitで実行します。

```bash
streamlit run src/main.py
```

2. ブラウザで表示される画面から
   - CSVファイルを選択
   - 経路データを編集
   - 出発地・目的地・時給を指定
   - 「経路計算」ボタンで最適経路を表示

## データファイル

- `data/input.csv` などのCSVファイルに、`u,v,cost,time,method` 形式で経路情報を記述します。
- サンプルデータが `data/` フォルダに複数入っています。

## 依存パッケージ

- networkx
- pandas
- streamlit

## 開発ファイル構成

- `src/main.py` ... Streamlitアプリ本体
- `src/Edge.py` ... 経路（Edge）クラス定義
- `data/` ... 経路データCSV

