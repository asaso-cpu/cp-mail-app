from flask import Flask, request, render_template, jsonify
import json
import os
from crypto_util import encrypt_password  # 暗号化ユーティリティをインポート
import subprocess  # 外部コマンド実行用

app = Flask(__name__)

# ホームページを表示
@app.route('/')
def index():
    return render_template('index.html')

# フォームデータを受け取るエンドポイント
@app.route('/save', methods=['POST'])
def save_data():
    raw_password = request.form['password']
    encrypted_password = encrypt_password(raw_password)  # パスワード暗号化

    # 新しいユーザーデータの構築
    new_user_data = {
        'user_id': request.form['user_id'],
        'password': encrypted_password,
        'recipient_email': request.form['recipient_email'],
        'schedule': request.form['schedule']
    }

    # 既存のuser_data.jsonを読み込む（存在しない場合は空リスト）
    if os.path.exists('user_data.json'):
        try:
            with open('user_data.json', 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except json.JSONDecodeError:
            existing_data = []
    else:
        existing_data = []

    # 新しいデータを追加
    existing_data.append(new_user_data)

    # 保存
    with open('user_data.json', 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

    # CPmail.py 実行
    try:
        subprocess.run(['python', 'CPmail.py'], capture_output=True, text=True)
    except Exception as e:
        print("CPmail.py 実行中にエラー:", e)
        return jsonify({'message': 'データ保存は成功しましたが、CPmail.pyの実行に失敗しました。'})

    return jsonify({'message': 'データが保存され、CPmail.pyが実行されました!'})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)