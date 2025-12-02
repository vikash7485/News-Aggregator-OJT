#!/bin/bash
# Vercel build script - handles SQLite limitation
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
# Vercel doesn't have SQLite, so we'll manually collect static files
# or use a workaround

# Create staticfiles directory
mkdir -p staticfiles

# Copy static files manually (if static directory exists)
if [ -d "static" ]; then
    echo "Copying static files..."
    cp -r static/* staticfiles/ 2>/dev/null || true
fi

# Try to run collectstatic with --skip-checks (may still fail due to SQLite)
python manage.py collectstatic --noinput --skip-checks 2>/dev/null || {
    echo "Note: collectstatic skipped (SQLite not available on Vercel)"
    echo "Static files will be served from static/ directory"
}

echo "Build completed successfully!"

