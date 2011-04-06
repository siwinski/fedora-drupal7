#!/bin/bash
cd /etc/drupal7
for i in `ls -1`; do
mv $i/files /var/lib/drupal7/files/$i
/sbin/restorecon /var/lib/drupal7/files/$i
ln -s /var/lib/drupal7/files/$i /etc/drupal7/$i/files
done
