import csv
import os

class csv_writer:

    filepath = ''
    writer = csv.DictWriter


    def createFile(self, path, header):
        self.filepath = path
        self.header = header
        if(not os.path.exists(self.filepath)):
            with open(self.filepath, 'x', encoding='UTF8', newline='') as f:
                self.writer = csv.DictWriter(f, fieldnames=self.header)
                self.writer.writeheader()


    def writeRow(self, data):
        with open(self.filepath, 'a', encoding='UTF8', newline='') as f:
            self.writer = csv.DictWriter(f, fieldnames= self.header)
            self.writer.writerow(data)
    
