import loader
import asyncio
import logging
from handlers.user import handlers



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    loader.dp.include_routers( handlers.router)
    await loader.bot.delete_webhook(drop_pending_updates=True)
    await loader.dp.start_polling(loader.bot, allowed_updates=loader.dp.resolve_used_update_types())
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
