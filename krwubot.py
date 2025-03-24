import asyncio
import logging
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

logging.basicConfig(level=logging.INFO)

TOKEN = '7729692247:AAF7tAZtFfjBTM1U-iVF5A5lKluLS29i4Yo'
CHAT_IDS = [-1002524199201, 6174491209, -4625489957]

bot = Bot(token=TOKEN)

async def broadcast_message(text):
    for chat_id in CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            logging.info(f"{chat_id}로 메시지 전송 완료.")
        except Exception as e:
            logging.error(f"{chat_id} 메시지 전송 실패: {e}")

async def send_weekly_report():
    await broadcast_message('이번주도 수고많으셨습니다. 주간활동보고 부탁드립니다.')

async def send_current_time():
    now = datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
    await broadcast_message(f'현재 시각은 {now}입니다.')

async def main():
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Asia/Seoul'))

    scheduler.add_job(send_weekly_report, 'cron', day_of_week='fri', hour=15, minute=0)
    scheduler.add_job(send_current_time, 'interval', minutes=1)

    scheduler.start()

    logging.info("krwubot이 실행되었습니다.")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())