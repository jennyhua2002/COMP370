file size: 4870970 bytes

structure: "title","writer","pony","dialog"

number of episodes: 196
cd /home/ubuntu/repos/COMP370/HW4 && cut -d',' -f1 clean_dialog.csv | tail -n +2 | sort | uniq | wc -l 
OR    
awk -F',' 'NR>1 {print $1}' clean_dialog.csv | sort | uniq | wc -l


get all episodes: cd /home/ubuntu/repos/COMP370/HW4 && cut -d',' -f1 clean_dialog.csv | tail -n +2 | sort | uniq:

unexpected aspect of dataset: sometimes one episode has multiple writers, separated by , or ; or & could be confusing