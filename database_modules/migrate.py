from database_modules.database import migrate_all, verify_migrations

if __name__ == "__main__":
    migrate_all()
    verify_migrations()
