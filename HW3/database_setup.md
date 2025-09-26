# MariaDB Database Server Setup on EC2 - COMP370 Homework 3

## Overview
This document explains the complete setup process for configuring a MariaDB database server on an EC2 instance to run on port 6002, with a specific database and user for external access.

## Objectives Achieved
✅ Install MariaDB database server  
✅ Configure database to run on port 6002  
✅ Create empty database named "comp370_test"  
✅ Add user "comp370" with password "$ungl@ss3s"  
✅ Grant permissions to access comp370_test database  
✅ Configure firewall for external access  
✅ Make MariaDB publicly accessible  

## Step-by-Step Configuration Process

### 1. MariaDB Installation
```bash
sudo apt update
sudo apt install mariadb-server mariadb-client -y
```
- **Purpose**: Install MariaDB server and client packages
- **Result**: MariaDB 10.11.13 installed with all dependencies
- **Service**: Automatically started and enabled on boot

### 2. Port Configuration
Modified `/etc/mysql/mariadb.conf.d/50-server.cnf`:
```bash
# Backup original configuration
sudo cp /etc/mysql/mariadb.conf.d/50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf.backup

# Add port configuration
sudo sed -i '/\[mysqld\]/a port = 6002' /etc/mysql/mariadb.conf.d/50-server.cnf

# Configure to bind to all interfaces for external access
sudo sed -i '/port = 6002/a bind-address = 0.0.0.0' /etc/mysql/mariadb.conf.d/50-server.cnf
```
- **Purpose**: Configure MariaDB to listen on port 6002 instead of default 3306
- **External Access**: Set bind-address to 0.0.0.0 to accept connections from any IP
- **File Modified**: `/etc/mysql/mariadb.conf.d/50-server.cnf`

### 3. Service Restart
```bash
sudo systemctl restart mariadb
```
- **Purpose**: Apply configuration changes
- **Verification**: Check with `sudo ss -tlnp | grep :6002`

### 4. Security Configuration
```bash
sudo mysql_secure_installation
```
- **Purpose**: Secure the MariaDB installation
- **Actions Taken**:
  - Removed anonymous users
  - Kept root login enabled for remote access
  - Reloaded privilege tables

### 5. Database Creation
```bash
sudo mysql -e "CREATE DATABASE comp370_test;"
```
- **Purpose**: Create the required empty database
- **Database Name**: `comp370_test`
- **Status**: Empty database ready for use

### 6. User Creation and Permissions
```bash
# Create user with specified password
sudo mysql -e "CREATE USER 'comp370'@'%' IDENTIFIED BY '\$ungl@ss3s';"

# Grant all privileges on comp370_test database
sudo mysql -e "GRANT ALL PRIVILEGES ON comp370_test.* TO 'comp370'@'%';"

# Apply changes
sudo mysql -e "FLUSH PRIVILEGES;"
```
- **User**: `comp370`
- **Password**: `$ungl@ss3s`
- **Access**: All privileges on `comp370_test` database
- **Host**: `%` (allows connections from any IP address)

### 7. Firewall Configuration
```bash
sudo ufw allow 6002/tcp
```
- **Purpose**: Allow incoming TCP traffic on port 6002
- **Security**: Only allows the specific port needed for database access

## Verification Steps

### 1. Service Status Check
```bash
sudo systemctl status mariadb
```
- **Result**: Service is active and running

### 2. Port Listening Verification
```bash
sudo ss -tlnp | grep :6002
```
- **Expected Output**: `LISTEN 0 80 0.0.0.0:6002 0.0.0.0:*`
- **Result**: MariaDB is listening on all interfaces on port 6002

### 3. Database Connection Test
```bash
mysql -u comp370 -p'$ungl@ss3s' -P 6002 -h localhost -e "SHOW DATABASES;"
```
- **Expected Output**: Shows `comp370_test` and `information_schema`
- **Result**: ✅ User can connect and see databases

### 4. Database Access Test
```bash
mysql -u comp370 -p'$ungl@ss3s' -P 6002 -h localhost comp370_test -e "SHOW TABLES;"
```
- **Expected Output**: Empty (no tables)
- **Result**: ✅ User can access the empty database

## Connection Information

### Local Access
- **Host**: localhost
- **Port**: 6002
- **Username**: comp370
- **Password**: $ungl@ss3s
- **Database**: comp370_test

### External Access
- **Host**: [EC2_PUBLIC_IP]
- **Port**: 6002
- **Username**: comp370
- **Password**: $ungl@ss3s
- **Database**: comp370_test

## Security Considerations

### 1. EC2 Security Groups
**CRITICAL**: You must configure your EC2 Security Group in the AWS Console:
1. Go to EC2 Dashboard → Security Groups
2. Select your instance's security group
3. Add inbound rule:
   - Type: Custom TCP
   - Port: 6002
   - Source: 0.0.0.0/0 (or specific IP ranges for better security)
   - Description: "MariaDB database server on port 6002"

### 2. Database Security
- User `comp370` has access only to `comp370_test` database
- Password contains special characters for security
- Root user remains accessible for administration

### 3. Network Security
- Firewall configured to allow only port 6002
- MariaDB configured to accept connections from any IP
- Consider restricting source IPs in production environments

## Database Client Setup (DBeaver)

### Connection Parameters for DBeaver:
- **Server Host**: [Your EC2 Public IP]
- **Port**: 6002
- **Database**: comp370_test
- **Username**: comp370
- **Password**: $ungl@ss3s
- **Driver**: MariaDB/MySQL

### Testing Connection:
1. Install DBeaver on your personal computer
2. Create new connection with above parameters
3. Test connection - should succeed
4. Browse to `comp370_test` database
5. Verify it's empty (no tables)

## Troubleshooting

### Common Issues
1. **Cannot connect from external client**:
   - Check EC2 Security Group settings
   - Verify MariaDB is listening on 0.0.0.0:6002
   - Ensure firewall allows port 6002

2. **Access denied errors**:
   - Verify username and password
   - Check user permissions: `sudo mysql -e "SHOW GRANTS FOR 'comp370'@'%';"`
   - Ensure FLUSH PRIVILEGES was run

3. **Service not starting**:
   - Check configuration syntax: `sudo mysql --help`
   - Review error logs: `sudo journalctl -u mariadb`

4. **Port not listening**:
   - Verify configuration in `/etc/mysql/mariadb.conf.d/50-server.cnf`
   - Check if service restarted after config changes

## Files Modified/Created
- `/etc/mysql/mariadb.conf.d/50-server.cnf` - Port and bind-address configuration
- `/etc/mysql/mariadb.conf.d/50-server.cnf.backup` - Backup of original config
- Database `comp370_test` - Created empty database
- User `comp370` - Created with specified password and permissions

## Configuration Summary
```ini
[mysqld]
port = 6002
bind-address = 0.0.0.0
```

## Next Steps for External Access
1. **Get your EC2 public IP**: Check AWS Console or use `curl ifconfig.me`
2. **Configure Security Group**: Add inbound rule for port 6002
3. **Test with DBeaver**: Connect using the connection parameters above
4. **Verify access**: Should be able to connect and see empty `comp370_test` database

## Summary
The MariaDB database server is now successfully configured to run on port 6002 with:
- Empty database `comp370_test` created
- User `comp370` with password `$ungl@ss3s` 
- Full permissions on the test database
- External access enabled
- Firewall configured

The final step is to configure the EC2 Security Group to allow external access to port 6002, after which you can connect from DBeaver or any other database client.
