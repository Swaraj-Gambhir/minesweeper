from tkinter import Button,Label
import random
import settings
import ctypes
import sys

class Cell:
    all=[]
    cell_count_label_object=None
    cell_count=settings.CELL_COUNT
    def __init__(self,x,y,is_mine=False):
        self.is_mine=is_mine
        self.cell_btn_object = None
        self.x=x
        self.y=y
        self.visited=False
        self.is_opened=False
        self.is_mine_candidate = False
        Cell.all.append(self)
    @staticmethod
    def gameover():
        ctypes.windll.user32.MessageBoxW(0,'You won the game','Game Over',0)
        sys.exit()
        
    def create_btn_object(self,location):
        btn= Button(
                location,
                bg='green',
                width=25,
                height=5
        )
        btn.bind('<Button-1>',self.left_click_actions)
        btn.bind('<Button-3>',self.right_click_actions)
        self.cell_btn_object=btn
    @staticmethod
    def create_cell_count_label(location):
        lbl=Label(
            location,
            text=f"Cells Left:{settings.CELL_COUNT}",
            width=25,
            height=5,
            font=("",24)
        )
        Cell.cell_count_label_object=lbl
        
    def left_click_actions(self,event):
        if self.is_mine:
            print("Its a mine")
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length==0:
                li=[self]
                while(len(li)!=0):
                    
                    cell=li.pop()
                    cell.visited=True
                    for cell_obj in cell.surrounded_cells:
                        cell_obj.show_cell()
                        
                        if cell_obj.surrounded_cells_mines_length==0:
                            print("Got Ya")
                            if cell_obj.visited==False:
                                li.append(cell_obj)
                    print(li)
            self.show_cell()
        self.cell_btn_object.unbind('<Button-1>',self.left_click_actions)
        self.cell_btn_object.unbind('<Button-3>',self.right_click_actions)
    def get_cell_by_axis(self,x,y):
        for cell in Cell.all:
            if cell.x==x and cell.y==y:
                return cell
    
    def right_click_actions(self,event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg='orange')
            self.is_mine_candidate=True
        else:
            self.cell_btn_object.configure(bg='green')
            self.is_mine_candidate=False



    @property
    def surrounded_cells(self):
        cells=[
            self.get_cell_by_axis(self.x-1,self.y-1),
            self.get_cell_by_axis(self.x-1,self.y),
            self.get_cell_by_axis(self.x-1,self.y+1),
            self.get_cell_by_axis(self.x,self.y-1),
            self.get_cell_by_axis(self.x,self.y+1),
            self.get_cell_by_axis(self.x+1,self.y-1),
            self.get_cell_by_axis(self.x+1,self.y),
            self.get_cell_by_axis(self.x+1,self.y+1),
            ]
        cells = [cell for cell in cells if cell is not None]
        return cells
    def show_cell(self):
        # print(self.surrounded_cells)
        # print(self.surrounded_cells_mines_length)
        
        
        
        if not self.is_opened:
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            Cell.cell_count-=1
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}")
                if(Cell.cell_count==9):
                    Cell.gameover()
            self.cell_btn_object.configure(bg='SystemButtonFace')
        self.is_opened=True
        
    
    @property
    def surrounded_cells_mines_length(self):
        counter=0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter+=1
        return counter

    @staticmethod
    def gameover():
        ctypes.windll.user32.MessageBoxW(0,'You won the game','Game Over',0)
        sys.exit()

    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0,'You clicked on a mine','Game Over',0)
        sys.exit()
    @staticmethod
    def randomize_mines():
        picked_cells=random.sample(Cell.all,settings.MINES_COUNT)
        print(picked_cells)
        for pcell in picked_cells:
            pcell.is_mine=True
    def __repr__(self):
        return f"Cell({self.x},{self.y})"
