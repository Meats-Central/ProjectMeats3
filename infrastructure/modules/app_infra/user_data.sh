#!/bin/bash

# ProjectMeats3 Cloud-Init Script for DigitalOcean Droplet
# This script sets up the application environment on Ubuntu 22.04

set -e

# Update system packages
apt update
apt upgrade -y

# Install Docker and Docker Compose
apt install -y docker.io docker-compose git curl

# Start and enable Docker service
systemctl start docker
systemctl enable docker

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Create application directory
mkdir -p /app
cd /app

# Clone the ProjectMeats3 repository
git clone https://github.com/Meats-Central/ProjectMeats3.git .

# Create environment file for production
cat > .env << 'EOF'
# Django settings
DEBUG=False
SECRET_KEY=change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database will be configured via environment variables from Terraform
# DATABASE_URL will be injected by the deployment process

# Security settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Logging
LOG_LEVEL=INFO
EOF

# Make setup script executable
chmod +x setup_env.py

# Set up Python environment and install dependencies
apt install -y python3 python3-pip python3-venv
pip3 install -r backend/requirements.txt

# Install Node.js and npm for frontend
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Install frontend dependencies
cd frontend
npm install
npm run build
cd ..

# Create systemd service for the application
cat > /etc/systemd/system/projectmeats.service << 'EOF'
[Unit]
Description=ProjectMeats3 Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/app
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=root

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl daemon-reload
systemctl enable projectmeats.service

# Create a script to start the application with database configuration
cat > /app/start_app.sh << 'EOF'
#!/bin/bash
# This script will be called after Terraform applies database configuration
cd /app

# Build and start the application
docker-compose up -d

# Wait for services to start
sleep 30

# Run database migrations
docker-compose exec -T backend python manage.py migrate

# Create superuser (only if it doesn't exist)
docker-compose exec -T backend python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@projectmeats.com', 'WATERMELON1219')
    print("Superuser created")
else:
    print("Superuser already exists")
PYEOF

echo "ProjectMeats3 application started successfully!"
EOF

chmod +x /app/start_app.sh

# Install UFW firewall and configure
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443
ufw allow 8000
ufw allow 3000

# Create log directory
mkdir -p /var/log/projectmeats
chmod 755 /var/log/projectmeats

echo "Cloud-init setup completed successfully!"
echo "Application directory: /app"
echo "Use /app/start_app.sh to start the application after configuring database connection"