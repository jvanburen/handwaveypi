class Grid:
    def __init__(self, values, WIDTH, HEIGHT):
        assert len(values) == WIDTH * HEIGHT
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.values = values
        

    def is_valid_pixel(self, r, c):
        return r >= 0 \
               and c >= 0 \
               and r < self.HEIGHT \
               and c < self.WIDTH
    
    def get_adj(self, pixel):
        "returns a list of coords one spot to the right &/or down (if any)"
        r = pixel // self.WIDTH
        c = pixel % self.WIDTH
        possible = {(r+1, c),
                    (r, c+1)}#,
##                    (r-1, c),
##                    (r, c-1)}
        
        return map(self.to_index,
                   (p for p in possible if self.is_valid_pixel(*p)))

    def to_index(self, coords):
        return self.WIDTH*coords[0] + coords[1]
    def __getitem__(self, index):
        return self.values[index]
    def __len__(self):
        return len(self.values)
    def __iter__(self):
        return iter(self.values)
