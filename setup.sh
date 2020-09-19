apt-get update
apt-get install python3-pip apache2 libapache2-mod-wsgi-py3 python3-dev libmariadb-dev default-mysql-client
pip3 install virtualenv
mkdir -p /django
cd /django
virtualenv ReadRecommend
source /django/ReadRecommend/bin/activate
cd /django/capstone-project-fab-5
pip install -r requirements.txt
echo 'Enter the vm IP address: '
read vm_ip_address
echo 'Enter the cloud mysql database IP address: '
read mysql_ip_address
sed -i s/35.197.179.188/$vm_ip_address/ mysite/mysite/settings.py
sed -i s/34.87.233.219/$mysql_ip_address/ mysite/mysite/settings.py
cp 000-default.conf /etc/apache2/sites-available
python mysite/manage.py migrate
mkdir -p mysite/media
python mysite/manage.py collectstatic
chown :www-data /django/debug.log
chmod g+w /django/debug.log
service apache2 restart
echo "If you didn't copy the three mysql SSL client certificates to /django, please copy and rerun setup.sh"
