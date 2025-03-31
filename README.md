# VMC Backend

Backend application for the VMC project.

## Default Admin User

A default admin user is automatically created when you start the application:

- Username: `sysadmin`
- Password: `12345678`
- Email: `1752476831@qq.com`

## Development Setup with Docker

### Prerequisites

- Docker
- Docker Compose

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vmc-backend
   ```

2. Start the containers:
   ```bash
   docker-compose up -d
   ```

   This will start:
   - MySQL (accessible at localhost:3306)
   - Redis (accessible at localhost:6379)
   - Application (accessible at localhost:8000)

3. To view logs:
   ```bash
   docker-compose logs -f
   ```

4. To stop the containers:
   ```bash
   docker-compose down
   ```

## Deployment on AWS EC2

### Prerequisites

- An AWS account
- An EC2 instance running Ubuntu 20.04 or later
- Basic understanding of AWS security groups and networking

### Setup Steps

1. Launch an EC2 instance:
   - Choose Ubuntu Server 20.04 LTS or later
   - Select an instance type (recommend t2.medium or better)
   - Configure security groups to allow:
     - SSH (port 22)
     - HTTP (port 80)
     - HTTPS (port 443)
     - Custom TCP (port 8000) - Only if you want direct access to the app

2. Connect to your instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. Install Docker and Docker Compose:
   ```bash
   # Update packages
   sudo apt update
   sudo apt upgrade -y

   # Install Docker
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   sudo apt update
   sudo apt install -y docker-ce
   sudo usermod -aG docker ${USER}

   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose

   # Apply group changes to current session
   newgrp docker
   ```

4. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vmc-backend
   ```

5. Deploy with Docker Compose:
   ```bash
   docker-compose up -d
   ```

6. (Optional) Set up Nginx as a reverse proxy:
   ```bash
   sudo apt install -y nginx

   # Create Nginx config
   sudo nano /etc/nginx/sites-available/vmc-backend
   ```

   Add the following configuration:
   ```
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/vmc-backend /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

7. (Optional) Set up SSL with Let's Encrypt:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### Production Considerations

1. Change default passwords in the docker-compose.yml file before deployment.
2. Use environment variables for sensitive information.
3. Set up backups for the MySQL data.
4. Configure monitoring for the application and infrastructure.
5. Consider using AWS RDS for MySQL and AWS ElastiCache for Redis in a production environment.

## Data Persistence

- MySQL data is stored in the `mysql_data` volume
- Redis data is stored in the `redis_data` volume
- Application file uploads are stored in the `./data` directory which is mounted to `/opt/data` in the container 

## Troubleshooting Database Migration Issues

When starting the application with Docker Compose for the first time, you might encounter database migration errors such as:
- `Table 'questionnaire_score_info' already exists`
- `Table 'db1.user_info' doesn't exist`

These issues occur due to inconsistencies in the migration state. Here are several solutions:

### Solution 1: Reset Database (For Development Environment)

If you don't need to preserve data, the simplest solution is to reset the database:

```bash
# Stop containers
docker-compose down

# Remove MySQL volume (WARNING: This will delete all data!)
docker volume rm vmc-backend_mysql_data

# Start again
docker-compose up -d
```

### Solution 2: Use the Robust Migration Script

For preserving data while fixing migration issues, use the robust migration scripts included in the repository:

```bash
# Ensure scripts are executable
chmod +x robust_migrations.py fix_questionnaire_score.py fix_migrations.sh

# Run the fix script
docker-compose exec app ./fix_migrations.sh
```

### Solution 3: Manual Migration Fixes

You can also manually fix specific migration issues:

```bash
# Connect to the application container
docker-compose exec app bash

# Inside the container, run these commands:
# For tables that already exist but need migration records
python manage.py migrate questionnaire_score --fake

# For missing tables that depend on existing tables
python manage.py migrate user --fake-initial

# Exit the container
exit
```

### Prevention Measures

To prevent migration issues in the future:

1. **Avoid manual database schema changes** - Let Django handle all migrations
2. **Backup your database** before major updates
3. **Use the robust migrations script** in `docker-entrypoint.sh`
4. **Create separate volumes** for development and production environments

If you frequently encounter migration issues, consider adding these scripts to your deployment workflow. 