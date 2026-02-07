import machine
import network
import urequests
from utime import sleep

print("\n\n")


def connect():
    ssid = None
    password = None

    try:
        for i in range(5, 0, -1):
            print(f"\rConnecting in {i}s. Press CTRL+C now to configure.", end="")
            sleep(1)
    except KeyboardInterrupt:
        print()
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

    print()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for i in range(120, 0, -1):
        if wlan.isconnected():
            break
        print(f"\rConnecting... ({i})", end="   ")
        sleep(1)
    print()

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
    update_url = get_update_url()
    if not update_url:
        print("no update url found in url.txt")
        return
    print(f"{update_url=}")
    local_etag = get_local_etag()

    print(f"{local_etag=}")

    try:
        print("Checking ETag...")
        res = urequests.request("HEAD", update_url)
        remote_etag = res.headers.get("ETag", "").replace("W/", "")
        res.close()

        print(f"{remote_etag=}")

        if remote_etag and remote_etag != local_etag:
            print(f"New version detected ({remote_etag}). Downloading...")

            res = urequests.get(update_url)
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

print("starting main...")
