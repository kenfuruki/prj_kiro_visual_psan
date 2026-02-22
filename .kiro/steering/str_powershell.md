---
inclusion : always
---


## PowerShell 初期操作（新規セッション開始時のみ）

新しいターミナルセッションを開いた最初の1回だけ実行する。セッションが継続している間は不要。

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

```
## python仮想環境の設定
仮想環境がアクティブじゃない場合には、アクティブにする。
```powershell
.venv\Scripts\Activate.ps1
```