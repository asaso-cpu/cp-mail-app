document.getElementById('userForm').addEventListener('submit', function (e) {
    e.preventDefault();
    document.getElementById("message").innerText = "設定した時刻にメールを送ります！";
    const formData = new FormData(this);

    fetch('/save', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Flaskからのメッセージを表示
    })
    .catch(error => {
        console.error('送信エラー:', error);
        alert('データ送信に失敗しました');
    });
});

