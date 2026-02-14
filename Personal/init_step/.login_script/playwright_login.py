import sys, time, logging, os, subprocess, urllib.request
from playwright.sync_api import sync_playwright, TimeoutError, Error


# 配置日志
logging.basicConfig(
    filename="/tmp/login_wifi.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# logging.info(os.environ)
TARGET_URL = "http://192.168.2.1:3990"
USERNAME = "BLU707"
PASSWORD = "8949"
MAX_RETRIES = 12
RETRY_DELAY = 10  # 秒

def check_reachable(url, timeout=2):
    """用 requests 检查目标是否可达"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status < 500
    except Exception:
        return False


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            if len(sys.argv) > 1 and sys.argv[1] == "logoff":
                # 执行断开操作
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        page.goto(f"{TARGET_URL}/logoff")
                        logging.info("已执行断开连接")
                        break
                    except Error as e:
                        logging.warning(f"断开失败（第{attempt}次）：{e}")
                        if attempt < MAX_RETRIES:
                            time.sleep(RETRY_DELAY)
                        else:
                            raise
            else:
                for attempt in range(1, MAX_RETRIES + 1):
                    # 正常登录前先关闭 Captive Network Assistant
                    try:
                        subprocess.run(
                            ["pkill", "-f", "Captive Network Assistant"],
                            check=False,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        logging.info("已关闭 Captive Network Assistant")
                    except Exception as e:
                        logging.warning(f"关闭 Captive Network Assistant 失败: {e}")
                    if not check_reachable(TARGET_URL):
                        logging.warning(f"目标不可达，等待重试（第{attempt}次）")
                        time.sleep(RETRY_DELAY)
                        continue

                    try:
                        page.goto(TARGET_URL, timeout=5000)
                        page.wait_for_selector('input[name="UserName"]', timeout=1500)
                        page.fill('input[name="UserName"]', USERNAME)
                        page.fill('input[name="Password"]', PASSWORD)
                        page.click('input[type="submit"]')
                        page.wait_for_timeout(1000)
                        logging.info("登录成功")
                        break
                    except TimeoutError:
                        logging.info("已登录，无需操作")
                        break
                    except Error as e:
                        logging.warning(f"登录失败（第{attempt}次）：{e}")
                        if attempt < MAX_RETRIES:
                            time.sleep(RETRY_DELAY)
                        else:
                            raise

        except Exception as e:
            logging.error(f"执行出错: {e}", exc_info=True)
            sys.exit(1)
        finally:
            browser.close()
            logging.info("浏览器已关闭")

    sys.exit(0)

if __name__ == "__main__":
    main()
