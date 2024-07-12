import subprocess
import webbrowser
import time

class QRProcessor(object):

    def __init__(self):
        self.prevmes = ""
        self.parsed = False
        return
    
    def parse_html(self, url):
        """
        面倒なのでいったんブラウザを開くだけにしておく
        """
        webbrowser.open(url)
        return

    def parse(self, mes):
        """
        sample:
        WIFI:S:switch_xxxxxxxxxx;T:WPA;P:password;;
        """
        # 二重起動防止
        if self.parsed:
             return False
        if mes == self.prevmes:
            return False
        self.parsed = True

        # QRコードの内容からSSIDとパスワードを取得する
        tmp = mes.split(';')
        ssid = tmp[0].split(':')[2]
        password = tmp[2].split(':')[1]
        print(f'SSID:{ssid}, password:{password}')
        
        # wifi登録コマンド
        register_cmd = f'netsh wlan set profileparameter name={ssid} keyMaterial={password}'
        print("register wifi")
        subprocess.call(register_cmd)
        time.sleep(5)
        # wifi 接続コマンド（上のは1回でよいけどチェックするのも面倒なので都度両方呼ぶ）
        set_cmd = f'netsh wlan connect name={ssid}'
        print(f'connect wifi:{ssid}')
        subprocess.call(set_cmd)
        # sleepは必要、時間は要検討
        time.sleep(10)

        # url open
        url = "http://192.168.0.1/index.html"
        self.parse_html(url)

        return self.parsed