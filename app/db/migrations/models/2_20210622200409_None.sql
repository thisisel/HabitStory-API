-- upgrade --
CREATE TABLE IF NOT EXISTS "rewards" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "tag" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "stories" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "tag" TEXT NOT NULL,
    "author" VARCHAR(100) NOT NULL,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "is_superuser" INT NOT NULL  DEFAULT 0,
    "is_verified" INT NOT NULL  DEFAULT 0,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "joined_date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
CREATE TABLE IF NOT EXISTS "challenges" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(100) NOT NULL  DEFAULT 'misc',
    "description" TEXT NOT NULL,
    "duration" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" CHAR(36) REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "journals" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "is_public" INT NOT NULL  DEFAULT 0,
    "streak" INT NOT NULL  DEFAULT 0,
    "started" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "finished" TIMESTAMP,
    "active" INT NOT NULL  DEFAULT 1,
    "last_modified" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "challenge_id" INT NOT NULL REFERENCES "challenges" ("id") ON DELETE RESTRICT,
    "reward_id" INT NOT NULL REFERENCES "stories" ("id") ON DELETE RESTRICT,
    CONSTRAINT "uid_journals_author__8439e3" UNIQUE ("author_id", "challenge_id")
);
CREATE TABLE IF NOT EXISTS "pages" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "day_num" INT NOT NULL,
    "submitted" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_modified" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "note" TEXT,
    "journal_id" INT NOT NULL REFERENCES "journals" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
