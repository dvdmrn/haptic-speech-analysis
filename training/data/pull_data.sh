echo enter username:
read userName
scp -r $userName@remote.cs.ubc.ca:/ubc/cs/research/imager/project/spin/proj/haptic-speech/training/data/* .
