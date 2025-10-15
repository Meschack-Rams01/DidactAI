# Database Setup Guide for DidactAI

## Option 1: PostgreSQL on Render (Recommended for Production)

### Step 1: Create PostgreSQL Database
1. Go to your Render Dashboard
2. Click "New +" button
3. Select "PostgreSQL"
4. Choose a name: `didactai-db`
5. Select your plan (Free tier available)
6. Click "Create Database"

### Step 2: Get Database URL
After creation, Render will provide:
- **Internal Database URL**: `postgresql://username:password@hostname:port/database_name`
- Use the "Internal Database URL" for better performance

### Step 3: Add to Environment Variables
In your web service environment variables:
```
Key: DATABASE_URL
Value: [Your PostgreSQL Internal Database URL from Render]
```

## Option 2: SQLite (Simple, for development)

If you want to use SQLite (simpler setup):
```
Key: DATABASE_URL
Value: sqlite:///./db.sqlite3
```

## Option 3: External PostgreSQL Services

### Supabase (Free tier available)
1. Go to https://supabase.com
2. Create new project
3. Get connection string from Settings > Database
4. Format: `postgresql://user:password@host:port/database`

### ElephantSQL (Free tier available)
1. Go to https://www.elephantsql.com
2. Create free account and instance
3. Get the URL from instance details

### Neon (Free tier available)
1. Go to https://neon.tech
2. Create account and database
3. Get connection string

## Environment Variables Summary

Add these to your Render environment variables:

```
SECRET_KEY=KeLcXQZdNrAO=ga+u#q9*f0zai#ET@9(q)q-B0ThsYW=+H@S*M
DATABASE_URL=[Your chosen database URL]
DEBUG=False
ALLOWED_HOSTS=didactai.onrender.com,localhost,127.0.0.1
```

## Database Migration Commands

After setting up the database, you may need to run migrations.
Add this to your Render build command:

```bash
pip install -r requirements-deploy.txt && python manage.py migrate
```

Or use the startup script that handles this automatically.