import json
import csv

class metadata:
    def __init__(self):
        path  = '/home/ec2-user/Dataset/'
        self.scraped_genre = path+'MMD_scraped_genre.jsonl'
        self.audio_matches = path+'MMD_audio_matches.tsv'
        self.title_artist = path+'MMD_scraped_title_artist.jsonl'

        self.title_artist_data = {}
        self.md5_to_sid = {}

    #def get_title_artist(self):
        #title_artist
        with open(self.title_artist, 'rt', encoding='UTF8') as f:
            for line in f:
                l = json.loads(line)
                self.title_artist_data[l['md5']+'.mid'] = {'title':l['title_artist'][0][0], 'artist':l['title_artist'][0][1]} 
        # return self.title_artist

    #def get_sid(self):
        # Open the TSV file
        with open(self.audio_matches, "r") as file:
        # Create a CSV reader object
            reader = csv.reader(file, delimiter="\t")

            # Get the header row
            header = next(reader)

            # Iterate through each row in the file
            for row in reader:
                self.md5_to_sid[row[0]+'.mid'] = {header[i]: row[i] for i in range(1, len(header))}
        
        #return self.md5_to_sid

# for line in title_artist_data:
#     midi_name = line['md5'] + '.mid'
#     title = line['title_artist'][0][0]
#     artist = line['title_artist'][0][1]
    



