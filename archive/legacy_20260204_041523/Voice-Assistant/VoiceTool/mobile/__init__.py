# Wanda Voice Assistant - Mobile Package
"""Telegram Bot, Push Notifications, Remote Project Init."""

# Lazy imports to avoid circular dependencies
__all__ = ['WandaTelegramBot', 'WandaNotifier', 'ProjectInitializer']

def __getattr__(name):
    """Lazy loading of submodules."""
    if name == 'WandaTelegramBot':
        from mobile.telegram_bot import WandaTelegramBot
        return WandaTelegramBot
    elif name == 'WandaNotifier':
        from mobile.notifier import WandaNotifier
        return WandaNotifier
    elif name == 'ProjectInitializer':
        from mobile.project_init import ProjectInitializer
        return ProjectInitializer
    raise AttributeError(f"module 'mobile' has no attribute '{name}'")
