dirname=$(pwd)
dirname=${dirname##*/}
target="${HOME}/Dropbox/insight/project/"
echo "backing up $dirname to $target/$dirname/"
mkdir -p $target/$dirname
/usr/bin/rsync -avz * $target/$dirname/ \
--exclude '*~' \
--exclude '*.zip' \
--exclude '*.gz' \
--exclude '*.a' \
--exclude '*.o' \
--exclude '*.dat' \
--exclude '*.eps' \
--exclude '*.pdf' \
--exclude '*.png' \
--exclude '*/*.eps' \
--exclude '*/*.pdf' \
--exclude '*/*.png' \
