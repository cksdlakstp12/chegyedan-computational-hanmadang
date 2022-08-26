import glob
import cv2


class DataLoader():
    def __init__(self, path):
        self.path = path
        self.files = glob.glob(self.path)
        self.curr_image_path = self.files[0]
        self.idx = -1

    def load_next_image_path_label(self):
        self.idx += 1
        if not self.idx <= len(self.files) - 1:
            self.idx = len(self.files) - 1
            return None, None

        else:
            self.curr_image_path = self.files[self.idx]
            with open(self.curr_image_path.replace("jpg", "txt"), 'r') as f:
                text = f.readline()
            
            return self.curr_image_path, text

    def load_prev_image_path_label(self):
        self.idx -= 1
        if not self.idx >= 0:
            self.idx = -1
            return None, None

        else:
            self.curr_image_path = self.files[self.idx]
            with open(self.curr_image_path.replace("jpg", "txt"), 'r') as f:
                text = f.readline()
            
            return self.curr_image_path, text
    
    def reload_files(self):
        self.files = glob.glob(self.path)