from typing import List, Tuple

class FortyTwo:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.x = int((width/2) - 3)
        self.y = int((height/2) - 2)
    
    def get_cells(self) -> List[Tuple[int, int]]:
        if self.width < 14 or self.height < 10:
            # return impossible values if grid is too small
            return []
        four = [(self.x, self.y),
                (self.x, self.y+1),
                (self.x, self.y+2),
                (self.x+1, self.y+2),
                (self.x+2, self.y+2),
                (self.x+2, self.y+3),
                (self.x+2, self.y+4)]
        two = [(self.x+4, self.y),
                (self.x+5, self.y),
                (self.x+6, self.y),
                (self.x+6, self.y+1),
                (self.x+6, self.y+2),
                (self.x+5, self.y+2),
                (self.x+4, self.y+2),
                (self.x+4, self.y+3),
                (self.x+4, self.y+4),
                (self.x+5, self.y+4),
                (self.x+6, self.y+4)]
        return four + two