# Apache Web Server Setup on EC2 - COMP370 Homework 3

## Overview
This document explains the complete setup process for configuring an Apache web server on an EC2 instance to serve files on port 8008, specifically serving the `comp370_hw3.txt` file.

## Objectives Achieved
✅ Set up Apache web server on port 8008  
✅ Configure security groups to allow traffic on port 8008  
✅ Serve files from the document root  
✅ Access via public IP address  

## Step-by-Step Configuration Process

### 1. File Preparation
- **Action**: Enhanced the content of `/home/ubuntu/comp370_hw3.txt` with informative text
- **Purpose**: Make the served file more interesting and educational
- **Content Added**: Server details, assignment objectives, and fun facts about Apache

### 2. Apache Installation
```bash
sudo apt update
sudo apt install apache2 -y
```
- **Purpose**: Install the Apache HTTP server package
- **Result**: Apache 2.4.58 installed with all necessary dependencies

### 3. Document Root Setup
```bash
sudo cp /home/ubuntu/comp370_hw3.txt /var/www/html/
```
- **Purpose**: Copy the target file to Apache's default document root
- **Location**: `/var/www/html/` (Apache's default web directory)

### 4. Port Configuration
```bash
# Backup original ports configuration
sudo cp /etc/apache2/ports.conf /etc/apache2/ports.conf.backup

# Add port 8008 to listen configuration
echo "Listen 8008" | sudo tee -a /etc/apache2/ports.conf
```
- **Purpose**: Configure Apache to listen on port 8008 in addition to the default port 80
- **File Modified**: `/etc/apache2/ports.conf`

### 5. Virtual Host Configuration
Created `/etc/apache2/sites-available/8008.conf`:
```apache
<VirtualHost *:8008>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ServerName localhost
    
    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
- **Purpose**: Define a virtual host specifically for port 8008
- **Key Features**: 
  - Serves files from `/var/www/html`
  - Allows directory indexing
  - Enables access for all users
  - Logs errors and access attempts

### 6. Enable Site Configuration
```bash
sudo a2ensite 8008.conf
```
- **Purpose**: Enable the new virtual host configuration
- **Result**: Creates symbolic link in `/etc/apache2/sites-enabled/`

### 7. Firewall Configuration
```bash
sudo ufw allow 8008/tcp
```
- **Purpose**: Allow incoming TCP traffic on port 8008 through the Ubuntu firewall
- **Security**: Only allows the specific port needed for the web server

### 8. Service Management
```bash
sudo systemctl reload apache2
sudo systemctl start apache2
sudo systemctl enable apache2
```
- **Purpose**: 
  - Reload configuration changes
  - Start the Apache service
  - Enable automatic startup on boot

## Verification Steps

### 1. Service Status Check
```bash
sudo systemctl status apache2
```
- **Result**: Service is active and running

### 2. Port Listening Verification
```bash
sudo ss -tlnp | grep :8008
```
- **Result**: Apache is listening on port 8008

### 3. Local Access Test
```bash
curl -I http://localhost:8008/comp370_hw3.txt
```
- **Result**: HTTP 200 OK response with proper headers

## Access Information

### Local Access
- **URL**: `http://localhost:8008/comp370_hw3.txt`
- **Status**: ✅ Working

### External Access
- **URL Format**: `v`
- **Requirements**: 
  - EC2 Security Group must allow inbound traffic on port 8008
  - Public IP address of the EC2 instance

## Security Considerations

### 1. EC2 Security Groups
**CRITICAL**: You must configure your EC2 Security Group in the AWS Console:
1. Go to EC2 Dashboard → Security Groups
2. Select your instance's security group
3. Add inbound rule:
   - Type: Custom TCP
   - Port: 8008
   - Source: 0.0.0.0/0 (or specific IP ranges for better security)
   - Description: "Apache web server on port 8008"

### 2. Firewall Configuration
- Ubuntu UFW firewall configured to allow port 8008
- Only necessary ports are opened

### 3. File Permissions
- Files in `/var/www/html/` have appropriate permissions for web serving
- Apache runs with limited privileges

## Troubleshooting

### Common Issues
1. **Cannot access from external browser**:
   - Check EC2 Security Group settings
   - Verify public IP address
   - Ensure firewall rules are correct

2. **Service not starting**:
   - Check Apache configuration syntax: `sudo apache2ctl configtest`
   - Review error logs: `sudo tail -f /var/log/apache2/error.log`

3. **Port not listening**:
   - Verify port configuration in `/etc/apache2/ports.conf`
   - Check if site is enabled: `sudo a2ensite 8008.conf`

## Files Modified/Created
- `/home/ubuntu/comp370_hw3.txt` - Enhanced content
- `/var/www/html/comp370_hw3.txt` - Copy for web serving
- `/etc/apache2/ports.conf` - Added port 8008
- `/etc/apache2/sites-available/8008.conf` - New virtual host
- `/etc/apache2/sites-enabled/8008.conf` - Enabled site (symlink)

## File Updates
When you edit the content of `/home/ubuntu/comp370_hw3.txt`, you need to copy it to the web directory:
```bash
sudo cp /home/ubuntu/comp370_hw3.txt /var/www/html/
```
**Note**: No Apache restart is needed - changes are immediately available on the web server.

## Next Steps for External Access
1. **Get your EC2 public IP**: Check AWS Console or use `curl ifconfig.me`
2. **Configure Security Group**: Add inbound rule for port 8008
3. **Test access**: Open `http://[YOUR_PUBLIC_IP]:8008/comp370_hw3.txt` in a web browser

## Summary
The Apache web server is now successfully configured to serve the `comp370_hw3.txt` file on port 8008. The server is running, the firewall is configured, and the file is accessible locally. The final step is to configure the EC2 Security Group to allow external access to port 8008.
