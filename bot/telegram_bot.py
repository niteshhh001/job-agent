import os
import sys
import json
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from core.preferences import UserPreferences
from core.scorer import score_job


# =========================
# TOKEN (ENV VARIABLE ONLY)
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN not set. Please set environment variable BOT_TOKEN.")
    sys.exit(1)


# =========================
# SAFE FILE HELPERS
# =========================
def load_jobs():
    try:
        with open("data/normalized_jobs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def load_users():
    try:
        with open("data/users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


# =========================
# PROFILE PARSER (ENTITY-BASED)
# =========================
def parse_profile_text(text: str):
    """
    Parses structured user profile text into entities.
    """
    patterns = {
        "roles": r"role\s*:\s*(.+)",
        "locations": r"location\s*:\s*(.+)",
        "skills": r"skills\s*:\s*(.+)",
        "experience": r"experience\s*:\s*(\d+)",
        "salary": r"salary\s*:\s*(\d+)",
        "job_type": r"job\s*type\s*:\s*(.+)",
        "company_type": r"company\s*type\s*:\s*(.+)",
    }

    data = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()

            if key in ["roles", "locations", "skills"]:
                data[key] = [v.strip() for v in value.split(",") if v.strip()]
            elif key in ["job_type", "company_type"]:
                data[key] = value.lower()
            else:
                data[key] = int(value)

    return data


# =========================
# COMMAND HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Job Agent Bot!\n\n"
        "Commands:\n"
        "/setprofile – Set preferences in natural format\n"
        "/jobs – Get matching jobs\n\n"
        "Example:\n"
        "/setprofile\n"
        "role: backend engineer\n"
        "location: delhi, remote\n"
        "experience: 2 years\n"
        "salary: 15 lpa\n"
        "skills: python, api"
    )


async def setprofile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/setprofile", "").strip()
    profile = parse_profile_text(text)

    if "roles" not in profile or "locations" not in profile:
        await update.message.reply_text(
            "❌ Missing required fields.\n\n"
            "You must provide at least:\n"
            "role: ...\n"
            "location: ...\n\n"
            "Example:\n"
            "/setprofile\n"
            "role: software engineer\n"
            "location: delhi"
        )
        return

    user_id = str(update.effective_user.id)
    users = load_users()

    users[user_id] = {
        "roles": profile.get("roles", []),
        "locations": profile.get("locations", []),
        "skills": profile.get("skills", []),
        "experience": profile.get("experience"),
        "salary": profile.get("salary"),
        "job_type": profile.get("job_type"),
        "company_type": profile.get("company_type"),
    }

    save_users(users)

    await update.message.reply_text(
        "✅ Profile saved successfully!\n\n"
        f"Roles: {', '.join(users[user_id]['roles'])}\n"
        f"Locations: {', '.join(users[user_id]['locations'])}\n"
        f"Skills: {', '.join(users[user_id]['skills']) if users[user_id]['skills'] else 'None'}\n"
        f"Experience: {users[user_id].get('experience', 'N/A')} years\n"
        f"Salary: {users[user_id].get('salary', 'N/A')} LPA"
    )


async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_users()

    if user_id not in users:
        await update.message.reply_text(
            "⚠️ Profile not set.\nUse /setprofile first."
        )
        return

    prefs = users[user_id]

    preferences = UserPreferences(
        roles=prefs["roles"],
        locations=prefs["locations"],
        skills=prefs["skills"],
    )

    jobs_data = load_jobs()
    matched = []

    for job in jobs_data:
        score = score_job(job, preferences)
        if score > 0:
            matched.append({
                **job,
                "match_score": score
            })

    if not matched:
        await update.message.reply_text("😕 No matching jobs found.")
        return

    matched.sort(key=lambda x: x["match_score"], reverse=True)

    response = "🔥 Top Jobs for You:\n\n"

    for job in matched[:5]:
        response += (
            f"🏢 {job['company'].title()}\n"
            f"💼 {job['title']}\n"
            f"📍 {job['location']}\n"
            f"⭐ Match: {job['match_score']}\n"
            f"🔗 {job['apply_url']}\n\n"
        )

    await update.message.reply_text(response)


# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setprofile", setprofile))
    app.add_handler(CommandHandler("jobs", jobs))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
