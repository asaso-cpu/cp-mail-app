const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pyProc = null;

// Electronが開発中かビルド済みかを判定
const isDev = !app.isPackaged;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
        }
    });

    // Flaskサーバーにアクセス
    mainWindow.loadURL('http://127.0.0.1:5000');

    mainWindow.maximize();

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function startFlask() {
    // Flaskサーバーを起動するパスを切り替える
    const script = isDev
        ? path.join(__dirname, 'app.py')
        : path.join(process.resourcesPath, 'app.py');
    const cwd = isDev ? __dirname : process.resourcesPath;
        // Pythonプロセス起動
    pyProc = spawn('python', [script], { cwd, shell: true });

    pyProc.stdout.on('data', (data) => {
        console.log(`Flask stdout: ${data}`);
    });

    pyProc.stderr.on('data', (data) => {
        console.error(`Flask stderr: ${data}`);
    });

    pyProc.on('close', (code) => {
        console.log(`Flask process exited with code ${code}`);
    });
}

app.whenReady().then(() => {
    startFlask();
    createWindow();
});

app.on('window-all-closed', () => {
    if (pyProc) {
        pyProc.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
