"""
Migration: Clear Old S3 Avatar URLs
-----------------------------------
This script removes legacy S3-based avatar URLs from the users table.

It resets:
- avatar_url
- avatar_thumb_url

Only for rows where avatar_url contains 's3.amazonaws.com' or 'amazonaws.com'.

Safe to run multiple times.
"""

import os
from sqlalchemy import create_engine, text

# ------------------------------------------------------------
# Load DB connection string from environment or settings
# ------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)


def run_migration():
    print("\n=== SentinelOps Migration: Clear Old S3 Avatar URLs ===\n")

    with engine.connect() as conn:
        # Count affected rows
        count_query = text("""
            SELECT COUNT(*) FROM users
            WHERE avatar_url LIKE '%amazonaws.com%'
               OR avatar_thumb_url LIKE '%amazonaws.com%';
        """)
        result = conn.execute(count_query).scalar()

        print(f"Users with old S3 avatar URLs: {result}")

        if result == 0:
            print("No changes needed. Migration complete.\n")
            return

        # Perform update
        update_query = text("""
            UPDATE users
            SET avatar_url = NULL,
                avatar_thumb_url = NULL
            WHERE avatar_url LIKE '%amazonaws.com%'
               OR avatar_thumb_url LIKE '%amazonaws.com%';
        """)

        conn.execute(update_query)
        conn.commit()

        print(f"Cleared S3 avatar URLs for {result} user(s).")
        print("Migration complete.\n")


if __name__ == "__main__":
    run_migration()
