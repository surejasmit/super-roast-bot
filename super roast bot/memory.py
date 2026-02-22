from database import init_db, save_chat, get_recent_history, clear_db

# Initialize database on module load
init_db()

def add_to_memory(user_msg: str, bot_msg: str):
    """Saves to SQLite."""
    save_chat(user_msg, bot_msg)

def format_memory() -> str:
    """Fetches from SQLite and formats for the LLM."""
    history = get_recent_history(limit=10)
    if not history:
        return "No previous conversation."

    return "\n\n".join(
        [f"User: {u}\nAssistant: {b}" for u, b in history]
    )

def clear_memory():
    """Clears the SQLite table."""
    clear_db()