import sqlite3
from datetime import datetime
from instagram_api import post_to_instagram

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "YOUR_IG_ACCOUNT_ID"

def check_and_post():
    conn = sqlite3.connect("instagram_postplanner.db")
    c = conn.cursor()

    c.execute("SELECT id, image_path, caption, scheduled_time FROM scheduled_posts WHERE status = 'scheduled'")
    posts = c.fetchall()

    for post in posts:
        post_id, image_path, caption, scheduled_time = post
        scheduled_dt = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")
        if datetime.now() >= scheduled_dt:
            success = post_to_instagram(image_path, caption, ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID)
            if success:
                c.execute("UPDATE scheduled_posts SET status = 'posted' WHERE id = ?", (post_id,))
                conn.commit()

    conn.close()

if __name__ == "__main__":
    check_and_post()
