# UnsealEscape_v3
前回のコードからさらにリファクタリング＆要素追加を目指して
### 共通事項
#### キャラクターの歩行スプライトの順番：
0. 素
1. 右足出し
2. 素
3. 左足出し
#### 命名規則
全体として複数形の「s」はつけない方針  
**ローマ字とスペースを入れたファイルを作るな！**  
違うディレクトリでも名前被りは避けること（画像の連番は許す）  
拡張子：小文字！  
ファイル：スネークケース  
クラス：パスカルケース  
定数：大文字スネークケース  
フォルダ：できるだけ一単語、キャメルケース  
##### 変数
基本：できるだけ一単語、スネークケース  
bool：先頭にis_、has_などがあるスネークケース  
### 補足事項
.mdを改行する時は文末にスペースを2つ！  

### ビルド
ローカルでWindows版を作る場合：  
```powershell
python -m pip install -r requirements-build.txt
pyinstaller --noconfirm --clean UnsealEscape.spec
```
生成先は `dist/UnsealEscape.exe` です。`asset` フォルダの中身は実行ファイルに同梱されます。  

GitHub ActionsでWindows版とmacOS版を作る場合は、GitHubの **Actions** から **Build UnsealEscape** を選び、**Run workflow** を実行します。`v*` 形式のタグをpushした場合もビルドします。  
完了後、Actionsの実行ページにあるArtifactsから、Windows版またはmacOS版（Apple Silicon / Intel）をダウンロードできます。  
