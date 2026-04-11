class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __getitem__(self, index):
        return self.songs[index]

    def __len__(self):
        return len(self.songs)

playlist = Playlist(["Dancing Queen", "November Rain", "Barbie Girl"])

print(playlist[0])    
print(len(playlist)) 
