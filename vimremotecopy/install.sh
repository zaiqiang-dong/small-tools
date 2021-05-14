sudo cp ./rc.local /etc/
sudo cp ./rc-local.service /etc/systemd/system/
sudo systemctl enable rc-local
