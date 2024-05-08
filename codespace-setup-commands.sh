sudo apt update
sudo apt install libmariadb3 libmariadb-dev

mkdir -p /tmp/mdbccbin
cd /tmp/mdbccbin
curl -O https://downloads.mariadb.com/Connectors/c/connector-c-3.1.10/mariadb-connector-c-3.1.10-ubuntu-bionic-amd64.tar.gz
#echo "1b5b513f44967efadf5eae5e34952cd61f94655575d45b5a9182ea1b91d1d1fa  mariadb-connector-c-3.1.10-ubuntu-bionic-amd64.tar.gz" | sha256sum -c
# get root
sudo tar xvf mariadb-connector-c-3.1.10-ubuntu-bionic-amd64.tar.gz --directory /usr --strip-components 1
sudo echo "/usr/lib/mariadb/" > /etc/ld.so.conf.d/mariadb.conf
sudo ldconfig

pip install -r ./requirements.txt 