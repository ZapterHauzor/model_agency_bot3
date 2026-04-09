from app.core.config import settings

print("✅ Проверка настроек:")
print(f"  bot_token: {settings.bot_token[:10]}...{settings.bot_token[-5:]}")
print(f"  operator_chat_id: {settings.operator_chat_id}")
print(f"  usdt_wallet: {settings.usdt_wallet}")
print(f"  postgres_host: {settings.postgres_host}")
print(f"  redis_host: {settings.redis_host}")