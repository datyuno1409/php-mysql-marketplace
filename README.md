# PHP MySQL Marketplace

A complete e-commerce marketplace built with PHP and MySQL.

## Project Structure

```
├── admin/              # Admin panel files
├── assets/             # Static assets (favicon, archives)
├── backups/            # Database and system backups
├── configs/            # Configuration files
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── nginx.prod.conf
│   ├── nginx.ssl.conf
│   └── php-session.ini
├── database/           # SQL files and database scripts
│   ├── database.sql
│   ├── check-passwords.sql
│   ├── update-all-passwords.sql
│   └── update-passwords.sql
├── docs/               # Documentation
│   ├── README.md
│   ├── DEPLOYMENT.md
│   └── SUMMARY.md
├── includes/           # Common PHP includes
├── k8s/                # Kubernetes deployment files
├── login/              # Login functionality
├── logout/             # Logout functionality
├── scripts/            # Deployment and automation scripts
│   ├── backup-system.py
│   ├── deploy*.py
│   ├── cleanup-docker.py
│   └── k8s_status.py
├── seller/             # Seller panel files
├── signup/             # User registration
├── src/                # Frontend assets (CSS, JS, images)
└── ssl/                # SSL certificates
```

## Quick Start

### Development
```bash
cd configs
docker-compose up -d
```

### Production
```bash
cd configs
docker-compose -f docker-compose.prod.yml up -d
```

## Scripts

All deployment and automation scripts are located in the `scripts/` directory:

- `deploy.py` - Main deployment script
- `backup-system.py` - System backup utility
- `cleanup-docker.py` - Docker cleanup utility
- `k8s_status.py` - Kubernetes status checker

## Configuration

All configuration files are organized in the `configs/` directory:

- Docker configurations
- Nginx configurations
- PHP session settings

## Database

Database files and SQL scripts are in the `database/` directory:

- `database.sql` - Main database schema
- Password management scripts

## Documentation

Detailed documentation is available in the `docs/` directory.