# Pillar-sudoku - a simple toolkit for basic Sudoku generation & editing.

+ Generator:
  - [x] 3x3;
  - [x] 2x2;
  - [x] 3x2;
  - [x] 2x3;
  - [x] 4x4;
  - [x] custom sizes.
+ Custom characters to fill;
+ Checker:
  - [x] correct/incorrect;
  - [x] completed/not completed;
  - [ ] solver not implemented yet.
+ Getting rows/cells/columns/sectors;
+ Setting cells (only those that are missing).
<br><br>
> [!NOTE]
> _(It is only a toolkit, no GUI/TUI provided yet)._


<br><br>
## How to use?

### 1. **Creating Sudoku grid** <br>
  `any_name = Sudoku(sector_dimensions = [3, 3], fill_charset = "123456789", rnd_steps = 81)` <br>
  - `sector_dimenstions` : list : width, height;
  - `fill_charset`       : str  : symbols to fill the table;
  - `rnd_steps`          : int  : how many times are random functions executed when generating.
> [!IMPORTANT]
> + `width` and `height` must be > 2;
> + length of `fill_charset` must be equal to `width`×`height`;
> + `rnd_steps` must be > 0.
<br>

### 2. **Getting grid/sectors/columns/rows/cells** <br>
  - `get_row(n)` : row with index `n`;
  - `get_column(n)` : column with index `n`;
  - `get_sector(n)` : sector with index `n`;
  - `get_cell(n)` : cell with index `n`;
  - `get_grid()` : full grid.
> [!IMPORTANT]
> + `n` must be > 0 (numeration starts not with 0 but with 1);
> + functions return `list` (no nested lists in it).
<br>

### 3. **Setting cells' values** <br>
  - `set_cell(n, val)` : sets value `val` to cell with index `n`.
> [!IMPORTANT]
> + `n` must be > 0 (numeration starts not with 0 but with 1);
> + `val` must belong to `fill_charset`;
> + function sets value only if the cell was empty after the generation.
<br>

### 4. **Generating grid & removing numbers**
  - `generate()` : generates random Sudoku grid;
  - `remove(ratio)` : clears (`ratio`×100)% cells from full field.
> [!IMPORTANT]
> + `ratio` must be > 0 but < 1;
> + `generate()` generates **fully filled grid**, `remove()` removes random numbers.
<br>

### 5. **Checking grid**
  - `check()` : returns two `bool` 
    - `flag` - `True` if there are no mistakes, `False` otherwise;
    -  `complete` - `True` if all numbers are filled in, `False` otherwise.
> [!IMPORTANT]
> + `flag` - indicates **mistakes**;
> + `complete` - indicates whether the table is **full or not**.
<br>

## Gallery
![fully generated 3x3 sector Sudoku](https://github.com/user-attachments/assets/7f81440f-e2cd-4817-803b-d6bee881972a) <br>
**Fully generated Sudoku field (3x3 sector)**
<br><br>
![image](https://github.com/user-attachments/assets/c152f406-1225-4c71-858b-a27a09d32cf7) <br>
**Sudoku field with removed cells (ratio = 0.3)**

<br>

**...**

