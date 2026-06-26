import threading
from pynput import keyboard
import pystray
from PIL import Image, ImageDraw

# キー制御 (pynput)
# Windows環境でCapslock入力を無かったことにする
def win32_event_filter(msg, data):
    # CapsLockの仮想キーコードが20
    if data.vkCode == 20:
        listener.suppress_event() # 入力を消す
        return False # 他のアプリにキーイベントを渡さない
    return True

# Windows用のフィルターを適用してリスナーを初期化
listener = keyboard.Listener(win32_event_filter=win32_event_filter)


# タスクトレイアイコン (pystray)
def create_image():
    # 画像ファイルが無くても動くように
    image = Image.new('RGB', (64, 64), color='white')
    dc = ImageDraw.Draw(image)
    # バツ印
    dc.line((16, 16, 48, 48), fill='red', width=8)
    dc.line((16, 48, 48, 16), fill='red', width=8)
    return image

def on_quit(icon, item):
    listener.stop() # キー監視を停止
    icon.stop()     # アイコンを停止してアプリ終了

def setup_icon():
    # 右クリックメニュー
    menu = pystray.Menu(pystray.MenuItem('終了 (Quit)', on_quit))
    # アイコンの作成 (ホバー時にCapsLock Lockと表示)
    icon = pystray.Icon("CapsLockLock", create_image(), "CapsLock Lock", menu)
    icon.run()

if __name__ == '__main__':
    # キー監視を別スレッド（裏側）で開始
    listener.start()
    
    # メインスレッドでタスクトレイアイコンを実行（icon.run()が処理をブロックするため最後に記述）
    setup_icon()