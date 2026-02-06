import network
import urequests
from utime import sleep
import machine

print("\n\n")


def interrupt(msg, delay):
    print(msg)
    try:
        sleep(delay)
    except KeyboardInterrupt:
        return True
    return False


def connect():
    ssid = None
    password = None

    if interrupt(
        "Blocking for 5 seconds. Press CTRL+C now to configure wifi or updates", 5
    ):
        print("w - wifi")
        print("u - update url")
        print("x - exit")

        while 1:
            op = input("enter an option #:").strip()
            if op == "x":
                break
            elif op == "w":
                ssid = input("ssid:")
                password = input("password:")
            elif op == "u":
                url = input("update-url:").strip()
                with open("url.txt", "wt") as fp:
                    fp.write(url)

    print("connecting", end="")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(30):
        if wlan.isconnected():
            break
        print(".", end="")
        sleep(1)

    return wlan.isconnected()


def get_update_url():
    try:
        with open("url.txt") as f:
            return f.read().strip()
    except Exception:
        return ""


def get_local_etag():
    try:
        with open("etag.txt") as f:
            return f.read().strip()
    except Exception:
        return ""


def update_system():
    url = get_update_url()
    if not url:
        print("no update url found in url.txt")
        return
    local_etag = get_local_etag()

    try:
        print("Checking ETag...")
        res = urequests.request("HEAD", url)
        remote_etag = res.headers.get("ETag", "").replace("W/", "")
        res.close()

        if remote_etag and remote_etag != local_etag:
            print(f"New version detected ({remote_etag}). Downloading...")

            res = urequests.get(url)
            if res.status_code == 200:
                with open("main.py", "wb") as f:
                    while True:
                        chunk = res.raw.read(128)
                        if not chunk:
                            break
                        f.write(chunk)

                with open("etag.txt", "w") as f:
                    f.write(remote_etag)

                print("Update successful. Rebooting...")
                machine.reset()
        else:
            print("No updates found.")

    except Exception as e:
        print("Check failed:", e)


if connect():
    update_system()
