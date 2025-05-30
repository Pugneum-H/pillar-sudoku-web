"""Just simple toolkit used for basic sudoku generation & editing"""
import random

ERROR_VAL_INIT = "Invalid value. E.g. 'sector_dimensions' are always > 2 and 'fill_charset' is = sector_dimensions[0]*sector_dimensions[1] and 'rnd_steps' > 0"
ERROR_VAL_GET_N = "Invalid value. 'n' must always be > 0 and < sector's width*height when accessing rows and columns. Also value 'chr' should belong to 'fill_charset' and be 1 char length"
ERROR_VAL_RATIO = "Invalid value. 0 < ratio < 1."
ERROR_VAL_CHARSET = "Invalid value. No spaces allowed in fill_charset."

class Sudoku:
    """Sudoku class - used for everything"""
    def __init__(self, sector_dimensions : list[int] = [3,3], fill_charset : str = "123456789", rnd_steps : int = 81):
        if sector_dimensions[0] >= 2 and sector_dimensions[1] >= 2 and len(fill_charset) == sector_dimensions[0]*sector_dimensions[1] and rnd_steps > 0:
            self.__rnd_steps = rnd_steps
            self.__sector_width  = sector_dimensions[0]
            self.__sector_height = sector_dimensions[1]
            if " " in fill_charset: raise ValueError(ERROR_VAL_CHARSET)
            self.__fill_charset = fill_charset
            self.__grid = [str(_) for _ in range((self.__sector_width*self.__sector_height)**2)]
            self.__kept = [_ for _ in range((self.__sector_width*self.__sector_height)**2)]
        else:
            raise ValueError(ERROR_VAL_INIT)
    
    # Gets full grid
    def get_grid(self):
        return self.__grid
    
    # Gets row with idx N
    def get_row(self, n : int):
        if n > 0 and n <= self.__sector_width*self.__sector_height:
            return self.__grid[(n-1)*(self.__sector_width*self.__sector_height):n*(self.__sector_width*self.__sector_height):]
        else:
            raise ValueError(ERROR_VAL_GET_N)

    # Gets column with idx N
    def get_column(self, n : int):
        if n > 0 and n <= self.__sector_width*self.__sector_height:
            return self.__grid[n-1::(self.__sector_width*self.__sector_height)]
        else:
            raise ValueError(ERROR_VAL_GET_N)
    
    # Gets sector with idx N
    def get_sector(self, n : int):
        if n > 0 and n <= self.__sector_width*self.__sector_height:
            __t = []
            for i in range((n-1)//self.__sector_height*self.__sector_height+1, (n-1)//self.__sector_height*self.__sector_height+self.__sector_height+1, 1):
                __t.extend(self.get_row(i)[(self.__sector_height-1-(self.__sector_height*self.__sector_width-n)%self.__sector_height)*self.__sector_width : (self.__sector_height-1-(self.__sector_height*self.__sector_width-n)%self.__sector_height)*self.__sector_width + self.__sector_width])
            return __t
        else:
            raise ValueError(ERROR_VAL_GET_N)
    # Gets cell with idx N
    def get_cell(self, n : int):
        if n > 0 and n <= (self.__sector_width*self.__sector_height)**2:
            return self.__grid[n-1]
        else:
            raise ValueError(ERROR_VAL_GET_N)

    # Generating sudoku grid (all numbers are filled in)
    def generate(self):
        def __exchange_rows():
            __t1 = random.randint(0, self.__sector_width*self.__sector_height-1)
            __t2 = __t1
            while __t1 == __t2:
                __t2 = random.randint(__t1//self.__sector_height*self.__sector_height, __t1//self.__sector_height*self.__sector_height + self.__sector_height - 1)
            for i in range(self.__sector_width*self.__sector_height):
                self.__grid[__t1*self.__sector_width*self.__sector_height + i], self.__grid[__t2*self.__sector_width*self.__sector_height + i] = self.__grid[__t2*self.__sector_width*self.__sector_height + i], self.__grid[__t1*self.__sector_width*self.__sector_height + i]

        def __exchange_columns():
            __t1 = random.randint(0, self.__sector_width*self.__sector_height-1)
            __t2 = __t1
            while __t1 == __t2:
                __t2 = random.randint(__t1//self.__sector_width*self.__sector_width, __t1//self.__sector_width*self.__sector_width + self.__sector_width - 1)
            for i in range(self.__sector_width*self.__sector_height):
                self.__grid[__t1 + i * self.__sector_width*self.__sector_height], self.__grid[__t2 + i * self.__sector_width*self.__sector_height] = self.__grid[__t2 + i * self.__sector_width*self.__sector_height], self.__grid[__t1 + i * self.__sector_width*self.__sector_height]
            
        def __transpose():
            __t = self.__grid
            self.__grid = []
            for v in range(self.__sector_width * self.__sector_height):
                for h in range(self.__sector_width * self.__sector_height):
                    # print(f"{__t[h*self.__sector_width*self.__sector_height + v][0]} {v*self.__sector_width*self.__sector_height + h} {h*self.__sector_width*self.__sector_height + v}")
                    # self.__grid[v*self.__sector_width*self.__sector_height + h] = __t[h*self.__sector_width*self.__sector_height + v]
                    self.__grid.append(__t[h*self.__sector_width*self.__sector_height + v])
        
        def __exchange_sector_rows():
            __t01 = random.randint(0, self.__sector_width*self.__sector_height-1)
            __t02 = __t01
            while  __t02 in range(__t01//self.__sector_width*self.__sector_height, __t01//self.__sector_width*self.__sector_height + self.__sector_height):
                __t02 = random.randint(0, self.__sector_width*self.__sector_height-1)
            __t01 = __t01//self.__sector_height*self.__sector_width*self.__sector_height * self.__sector_height
            __t02 = __t02//self.__sector_height*self.__sector_width*self.__sector_height * self.__sector_height
            for rows in range(self.__sector_height):
                for cell in range(self.__sector_width*self.__sector_height):
                    self.__grid[__t01 + rows*self.__sector_width*self.__sector_height + cell], self.__grid[__t02 + rows*self.__sector_width*self.__sector_height + cell] = self.__grid[__t02 + rows*self.__sector_width*self.__sector_height + cell], self.__grid[__t01 + rows*self.__sector_width*self.__sector_height + cell]

        def __exchange_sector_columns():
            __t01 = random.randint(0, self.__sector_width*self.__sector_height-1)
            __t02 = __t01
            while  __t02 in range(__t01%self.__sector_height, self.__sector_width*self.__sector_height-2+__t01%self.__sector_height, self.__sector_height):
                __t02 = random.randint(0, self.__sector_width*self.__sector_height-1)
            for column in range(self.__sector_width):
                for cell in range(self.__sector_width*self.__sector_height):
                    self.__grid[__t01%self.__sector_height*self.__sector_width + column + cell*self.__sector_width*self.__sector_height], self.__grid[__t02%self.__sector_height*self.__sector_width + column + cell*self.__sector_width*self.__sector_height] = self.__grid[__t02%self.__sector_height*self.__sector_width + column + cell*self.__sector_width*self.__sector_height], self.__grid[__t01%self.__sector_height*self.__sector_width + column + cell*self.__sector_width*self.__sector_height]

        __t = random.randint(0, self.__sector_width*self.__sector_height - 1)
        self.__fill_charset = self.__fill_charset[__t:] + self.__fill_charset[:__t]
        self.__grid = [str(_) for _ in range((self.__sector_width*self.__sector_height)**2)]

        for vertical in range(0, self.__sector_width*self.__sector_height, 1):
            for horizontal in range(0, self.__sector_width*self.__sector_height, 1):
                self.__grid[vertical*self.__sector_width*self.__sector_height + horizontal] = (self.__fill_charset[(vertical%self.__sector_height)*self.__sector_width + vertical//self.__sector_height:] + self.__fill_charset[:(vertical%self.__sector_height)*self.__sector_width + vertical//self.__sector_height])[horizontal]

        for i in range(random.randint(self.__rnd_steps, self.__rnd_steps^2)):
            __exchange_rows()
        for i in range(random.randint(self.__rnd_steps, self.__rnd_steps^2)):
            __exchange_columns()
        for i in range(random.randint(self.__rnd_steps, self.__rnd_steps^2)):
            __transpose()
        for i in range(random.randint(self.__rnd_steps, self.__rnd_steps^2)):
            __exchange_sector_rows()
        for i in range(random.randint(self.__rnd_steps, self.__rnd_steps^2)):
            __exchange_sector_columns()

        return self.__grid
    # removes random cells with ratio 
    def remove(self, ratio : float = 0.5):
        rnd = 0
        if not(0 < ratio < 1): raise ValueError(ERROR_VAL_RATIO)
        else: 
            for i in range(int((self.__sector_width*self.__sector_height)**2 * ratio)):
                rnd = random.choice(self.__kept)
                self.__grid[rnd] = " "
                self.__kept.remove(rnd)
        return self.__grid


    # Sets cell with idx N if not kept
    def set_cell(self, n : int, val : str):
        if n > 0 and n <= (self.__sector_width*self.__sector_height)**2 and len(val) == 1 and (val in self.__fill_charset):
            if n-1 in self.__kept:
                pass
            else:
                self.__grid[n-1] = val 
        else:
            raise ValueError(ERROR_VAL_GET_N)
    

    # checks if sudoku is correct (all cells are unique in all rows, columns, sectors) returns flag and complete (correct -> True, incorrect -> False))
    def check(self):
        flag = False
        complete = True
        flag = all(
            len([i for i in self.get_row(u+1) if i != " "]) == len(set(i for i in self.get_row(u+1) if i != " ")) and
            len([i for i in self.get_column(u+1) if i != " "]) == len(set(i for i in self.get_column(u+1) if i != " ")) and
            len([i for i in self.get_sector(u+1) if i != " "]) == len(set(i for i in self.get_sector(u+1) if i != " "))
            for u in range(self.__sector_width * self.__sector_height)
        )
        for i in range((self.__sector_width*self.__sector_height)**2):
            if self.__grid[i] == " ": complete = False; break
       
        
        return flag, complete
    

    def set_grid(self, grid : list[str]):
        if all(_ in self.__fill_charset or _ == " " for _ in grid) and len(grid) == (self.__sector_width*self.__sector_height)**2:
            self.__grid = grid
