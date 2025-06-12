# CPメール通知アプリ

CoursePowerからの通知を自動取得し、ユーザーにメールでお知らせするデスクトップアプリです。

## 🎯 特徴
- Webサイトの課題・お知らせを自動取得
- ユーザー設定に基づいた通知送信（Gmail API使用）
- GUIベースの簡単な操作
- Python + Electronを使用

## 🖥️ 使用技術
- Python（Flask）
- Electron
- Gmail API
- BeautifulSoup（Webスクレイピング）

## 🛡️ セキュリティ対応
- `.env` によりAPIキーやURL等を管理
- 履歴からの機密情報除去済み（`git filter-repo`使用）

##　スクリーンショット
![CPmailアプリ画面 (1)](https://github.com/user-attachments/assets/8ac56b7e-d554-4211-95eb-346b7d72b18a)
![CPmailアプリ画面 (2)](https://github.com/user-attachments/assets/5280a036-e244-4706-b03f-c7b2fab60e90)
![CPmailアプリメール](https://github.com/user-attachments/assets/5258714d-366c-4057-983e-a284dcc76b41)

