"""
Companion/Sidekick system with encouraging messages.
"""
import random

# Available companions with their characteristics
COMPANIONS = {
    1: {
        'name': 'Wise Owl',
        'emoji': '🦉',
        'description': 'A wise mentor who guides you with ancient wisdom',
        'personality': 'wise and thoughtful'
    },
    2: {
        'name': 'Speedy Fox',
        'emoji': '🦊',
        'description': 'An energetic companion who celebrates your speed',
        'personality': 'energetic and quick'
    },
    3: {
        'name': 'Strong Bear',
        'emoji': '🐻',
        'description': 'A powerful friend who encourages perseverance',
        'personality': 'strong and steady'
    },
    4: {
        'name': 'Clever Cat',
        'emoji': '🐱',
        'description': 'A smart companion who appreciates creativity',
        'personality': 'clever and curious'
    },
    5: {
        'name': 'Brave Lion',
        'emoji': '🦁',
        'description': 'A courageous ally who inspires confidence',
        'personality': 'brave and bold'
    }
}

# Login messages (10 messages)
LOGIN_MESSAGES = [
    "Welcome back! Ready to conquer some exercises today? 💪",
    "Great to see you again! Your dedication is inspiring! ✨",
    "Hello! Let's make today count and learn something amazing! 🌟",
    "You're back! Time to continue your mathematical journey! 🚀",
    "Welcome! Every problem you solve makes you stronger! 💡",
    "Hey there! Your consistency is the key to mastery! 🔑",
    "Good to see you! Let's turn today into a learning adventure! 🎯",
    "You've returned! Remember, progress beats perfection! 📈",
    "Welcome! Your future self will thank you for studying today! 🌈",
    "Hi! Another day, another opportunity to grow! 🌱"
]

# Upload messages for small uploads (≤1 chapter worth of exercises)
UPLOAD_MESSAGES_SMALL = [
    "Nice work! Every exercise solved is a step forward! 🎯",
    "Well done! Consistency is more important than speed! ⭐",
    "Great job! You're building momentum! 🚀",
    "Excellent! Small steps lead to big achievements! 🌟",
    "Awesome! You're making steady progress! 💪",
    "Fantastic! Keep up this great rhythm! 🎵",
    "Wonderful! You're on the right track! 🛤️",
    "Impressive! Your dedication shows! 💎",
    "Brilliant! Every solution strengthens your skills! 🔧",
    "Amazing! You're doing better than you think! 🌈"
]

# Upload messages for large uploads (>1 chapter worth of exercises)
UPLOAD_MESSAGES_LARGE = [
    "WOW! You're on fire today! Incredible work! 🔥🔥🔥",
    "Outstanding! That's some serious dedication! 🏆",
    "Phenomenal! You're crushing it! 💥",
    "Spectacular! This is what excellence looks like! ⚡",
    "Unbelievable! You've made massive progress! 🚀🚀",
    "Extraordinary! Your work ethic is inspiring! 🌟✨",
    "Mind-blowing! You're setting the bar high! 📊",
    "Legendary! This is championship-level effort! 👑",
    "Magnificent! You're in beast mode! 🦁💪",
    "Astounding! You're unstoppable today! 🌪️"
]


def get_companion_info(companion_id):
    """Get companion information by ID."""
    return COMPANIONS.get(companion_id, COMPANIONS[1])


def get_login_message(companion_id):
    """Get a random login message with companion info as a dictionary."""
    companion = get_companion_info(companion_id)
    message = random.choice(LOGIN_MESSAGES)
    return {
        'emoji': companion['emoji'],
        'name': companion['name'],
        'message': message
    }


def get_upload_message(companion_id, is_large_upload=False):
    """
    Get a random upload message based on upload size.
    
    Args:
        companion_id: ID of the user's companion
        is_large_upload: True if uploading more than 1 chapter worth
    
    Returns:
        Dictionary with emoji, name, and message
    """
    companion = get_companion_info(companion_id)
    
    if is_large_upload:
        message = random.choice(UPLOAD_MESSAGES_LARGE)
    else:
        message = random.choice(UPLOAD_MESSAGES_SMALL)
    
    return {
        'emoji': companion['emoji'],
        'name': companion['name'],
        'message': message
    }


def get_all_companions():
    """Get list of all available companions for selection."""
    return COMPANIONS
