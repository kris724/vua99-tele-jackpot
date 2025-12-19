import requests
import time
from datetime import datetime, timedelta
API_URL = "https://api.bot88.com/api/v1/slot/jackpot"
BRAND_CODE = "bc5"

TELEGRAM_TOKEN = "8397765740:AAHp2ZTsWifRo9jUguH2qv9EB9rnnoA0uW8"
CHAT_ID = "-1002455512034"


last_status = {}
last_post_time = datetime.min 
last_message_id = None
def send_telegram(text, bold_ranges=[]):
    entities = []
    global last_message_id
    for start, length in bold_ranges:
        entities.append({
            "offset": start,
            "length": length,
            "type": "bold"
        })

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "entities": entities,
        "parse_mode": "HTML"
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        last_message_id = r.json()["result"]["message_id"]
    else:
        print("Telegram API lỗi:", r.text)
    
def get_jackpot():
    headers = {"x-brand-code": BRAND_CODE}
    r = requests.get(API_URL, headers=headers)
    return r.json()

def format_to_ty(number):
    ty = number / 1_000_000_000
    if ty.is_integer():
        return f"{int(ty)} Tỷ"
    else:
        return f"{ty:.1f} Tỷ"
def delete_last_message():
    global last_message_id
    if last_message_id:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteMessage"
        payload = {"chat_id": CHAT_ID, "message_id": last_message_id}
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            print("Xóa message lỗi:", r.text)
        last_message_id = None
def monitor():
    global last_status
    global last_post_time

    while True:
        try:
            data = get_jackpot()
            jackpot = data["data"]["big_jackpot"]

            exploded_games = [game for game, status in jackpot.items() if status]

            
            d = data["data"]

            jackpot_values = sum([d.get(game, 0) for game in exploded_games])
            Total_Amount = format_to_ty(jackpot_values)


            lines = []
            for game in exploded_games:
                value = d.get(game, 0)
                if value:
                    if game == "vgmn_100":
                        lines.append(f"🎲 Tài Xỉu: {value:,} đ - Đỉnh Nóc")
                    elif game == "qs_txgo-101_hitclub":
                        lines.append(f"🎮 Tài Xỉu Live: {value:,} đ - Kịch Trần")
                    elif game == "qs_xocdia-102_hitclub":
                        lines.append(f"☘️ Xóc Đĩa Live: {value:,} đ - Tài Lộc")
                    elif game == "vgcg_9":
                        lines.append(f"🍽 Xóc Đĩa: {value:,} đ")
                    elif game == "vgcg_14":
                        lines.append(f"🦀 Bầu Cua: {value:,} đ - Phát Tài")


            if datetime.now() - last_post_time >= timedelta(hours=4):
                delete_last_message()
                message = (
                    f"🎰 Hũ <b>{Total_Amount}</b> sắp nổ 💣🌈\n\n"
                    + "🎯 VUA99 đang có hũ cực khủng chờ bạn săn đây, nhanh tay đổi đời chỉ bằng 1 lượt quay 🔥\n\n"
                    + "\n".join(lines) + "\n\n"
                    + "🎁 <b>Đăng Ký Nhận Ngay:</b>\n\n"
                    + "✅ Thưởng nạp đầu 150%\n"
                    + "✅ Thưởng nạp lần hai 70%\n"
                    + "✅ 1.2% Hoàn trả không giới hạn.\n\n"
                    + "💥 B1: Tham Gia Nhóm Và Đừng Quên Add Bạn Bè\n"
                    + "💥 B2: Đăng Ký Ngay 🔗 <a href='https://vua99.com/?modal=SIGN_UP'>TẠI ĐÂY</a>\n"
                    + "💥 B3: Liên Hệ Nhận Ngay 🔞\n"
                    + "————\n"
                    + "💬 <a href=''>LIVE CHAT 24/7</a>\n"
                    + "👉 <a href='https://t.me/cskh_vua99'>TELEGRAM</a>\n"
                    + "▶️ <a href='https://www.youtube.com/@vua99official-3'>YOUTUBE</a>\n"
                    + "📲 <a href='https://www.facebook.com/VUA99.official/'>FB FANPAGE</a>\n"
                    + "#vua99 #bongda  #football #nohu #jackpot #slot #taixiu #baucua"
                )
                

                bold_start_1 = message.find("hận Ngay")
                bold_len_1 = len("Đăng Ký Nhận Ngay")
                bold_start_2 = message.find("Hũ")
                bold_len_2 = len("Hũ 52.3 Tỷ")
                send_telegram(message, bold_ranges=[(bold_start_1, bold_len_1),(bold_start_2, bold_len_2)])
                last_post_time = datetime.now()
                print("Notify exploded games:", exploded_games)
                print(last_message_id)
                

            last_status.update(jackpot)
            
        
        except Exception as e:
            print("Error:", e)

        time.sleep(5)

if __name__ == "__main__":
    monitor()
