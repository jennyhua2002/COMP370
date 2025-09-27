file size: 4870970 bytes
command: ls -la

structure: "title","writer","pony","dialog"
command: head -1 clean_dialog.csv 


number of episodes: 196
command:
cd /home/ubuntu/repos/COMP370/HW4 && cut -d',' -f1 clean_dialog.csv | tail -n +2 | sort | uniq | wc -l 
OR    
awk -F',' 'NR>1 {print $1}' clean_dialog.csv | sort | uniq | wc -l

get all episodes: cd /home/ubuntu/repos/COMP370/HW4 && cut -d',' -f1 clean_dialog.csv | tail -n +2 | sort | uniq:


unexpected aspect: one episode can have multiple writers, separated by , or ; or & , and multiple ponies speaking which can be confusing