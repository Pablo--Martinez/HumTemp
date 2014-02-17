echo Instalando xdrp...
sudo apt-get install xrdp
echo xdrp instalado correctamente!

echo Instalando Postgres...
sudo apt-get install postgresql
sudo service postgresql status
echo Postgres instalado correctamente!

echo Creando usuarios de base de datos...
sudo -u postgres createuser -PE -s root -W 'bioguardpassword'
sudo -u postgres createdb MapeoDB -O root
psql MapeoDB < backup.sql
echo Base de datos creada correctamente!

echo configurando GPIO...
cd bcm2835-1.25
./configure
make
sudo meke install
echo GPIO Configurado!

echo Configuración finalizada!


