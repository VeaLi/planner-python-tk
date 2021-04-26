# -*- coding: utf-8 -*-
"""
Created on Mon Sep 1 18:14:27 2020

@author: VinLes
"""

import tkinter as tk
import tkinter.simpledialog

from datetime import datetime, date
import calendar
import numpy as np
import joblib
from collections import defaultdict


def default():
    return []


# if you losd your data.dat run this:
'''
year = defaultdict(default)
year[2020] = defaultdict(default)
year[2020][1] = defaultdict(default)
year[2020][9] = defaultdict(default)
# 31 Jan 2020
year[2020][1][31] = ['Start the Coronavirus Pandemic']

year[2020][9][1] = ['Start of September',
                    'Go buy some flowers', 'Long text so long long task to do not enough though adding more lines to it']

joblib.dump(year, 'data\\data.dat')
'''


class PlannerApp():
    '''
    this is simple planner App
    '''

    def __init__(self):

        self.root = tk.Tk(className='SimplePlanner')

        self.CalendarData = joblib.load('data\\data.dat')

        self.today = datetime.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        _, self.nDaysInMonth = calendar.monthrange(self.year, self.month)

        self.dayWidth = 4
        self.weekRowStop = 0

        self.nOfFormerTasks = 0
        self.daySelected = None

        print(f'in current month {self.nDaysInMonth} days')

        self.construct()
        self.update()
        self.root.mainloop()

    def remove_plan(self, targetDay, k):
        del self.CalendarData[self.year][self.month][targetDay][k]

        joblib.dump(self.CalendarData, 'data\\data.dat')

        self.plan(targetDay)

    def add_plan(self, targetDay):
        newTask = tk.simpledialog.askstring(
            'Adding New Task', 'What\'s on your mind?')
        self.CalendarData[self.year][self.month][targetDay].append(newTask)

        joblib.dump(self.CalendarData, 'data\\data.dat')

        self.plan(targetDay)

    def plan(self, targetDay):

        for n in range(self.nOfFormerTasks):
            trow = self.weekRowStop+1+n
            l = list(self.root.grid_slaves(row=trow))
            for w in l:
                w.grid_forget()

        self.daySelected = targetDay
        print(f'date selected : {targetDay}')

        myPlansForThatYear = self.CalendarData[self.year]
        if myPlansForThatYear:
            myPlansForThatMonth = myPlansForThatYear[self.month]
            if myPlansForThatMonth:
                myPlansForThatDay = myPlansForThatMonth[targetDay]
                if myPlansForThatDay:
                    pass

                else:
                    self.CalendarData[self.year][self.month][targetDay] = []

            else:
                self.CalendarData[self.year][self.month] = defaultdict(default)
                self.CalendarData[self.year][self.month][targetDay] = []

        else:
            self.CalendarData[self.year] = defaultdict(default)
            self.CalendarData[self.year][self.month] = defaultdict(default)
            self.CalendarData[self.year][self.month][targetDay] = []

        print(f'plans for {targetDay}.{self.month}.{self.year} : {self.CalendarData[self.year][self.month][targetDay]}')

        self.nOfFormerTasks = len(
            self.CalendarData[self.year][self.month][targetDay])+1

        tk.Button(self.root, text=f'+', width=self.dayWidth, command=lambda d=targetDay: self.add_plan(d)).grid(row=self.weekRowStop+1, column=6, columnspan=1)
        for k, task in enumerate(self.CalendarData[self.year][self.month][targetDay]):
            if k == 0:
                tk.Button(self.root, text=f'+', width=self.dayWidth, command=lambda d=targetDay: self.add_plan(d)).grid(row=self.weekRowStop+1+k, column=6, columnspan=1)
            tk.Label(text=f'   {k+1}. {task}', wraplength=150).grid(row=self.weekRowStop+1+k+1, column=1, columnspan=6, sticky="W")
            tk.Button(self.root, text=f'-', width=self.dayWidth, command=lambda d=targetDay, k=k: self.remove_plan(d, k)).grid(row=self.weekRowStop+1+k+1, column=0, columnspan=1)

    def go_left(self):

        for n in range(self.nOfFormerTasks):
            trow = self.weekRowStop+1+n
            l = list(self.root.grid_slaves(row=trow))
            for w in l:
                w.grid_forget()

        if self.month-1 > 0:
            self.month -= 1
            _, self.nDaysInMonth = calendar.monthrange(self.year, self.month)
            self.construct()
        else:
            self.year -= 1
            self.month = 12
            _, self.nDaysInMonth = calendar.monthrange(self.year, self.month)
            self.construct()

    def go_right(self):

        for n in range(self.nOfFormerTasks):
            trow = self.weekRowStop+1+n
            l = list(self.root.grid_slaves(row=trow))
            for w in l:
                w.grid_forget()

        if self.month+1 < 13:
            self.month += 1
            _, self.nDaysInMonth = calendar.monthrange(self.year, self.month)
            self.construct()
        else:
            self.year += 1
            self.month = 1
            _, self.nDaysInMonth = calendar.monthrange(self.year, self.month)
            self.construct()

    def construct(self):

        for n in range(self.weekRowStop+1):
            l = list(self.root.grid_slaves(row=n))
            for w in l:
                w.grid_forget()

        weekRow = 1

        l = list(self.root.grid_slaves(row=weekRow))
        for w in l:
            w.grid_forget()

        tk.Button(self.root, text='<', width=self.dayWidth,
                  command=lambda: self.go_left()).grid(row=weekRow, column=0)
        tk.Button(self.root, text='>', width=self.dayWidth,
                  command=lambda: self.go_right()).grid(row=weekRow, column=6)

        thisMonth = calendar.month_name[self.month]
        tk.Label(text=f'{self.year}, {thisMonth}',).grid(row=weekRow, column=1, columnspan=5)

        weekNames = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

        weekRow = 2
        for k, wn in enumerate(weekNames):
            day = tk.Label(text=f'{wn}').grid(row=weekRow, column=k)

        weekRow = 3
        for i in range(1, self.nDaysInMonth+1):
            thatDay = date(self.year, self.month, i)
            thatDayName = calendar.day_name[thatDay.weekday()]
            thatDayCol = thatDay.weekday()
            day = None
            day = tk.Button(self.root, text=f'{i}', width=self.dayWidth, command=lambda d=i: self.plan(d)).grid(row=weekRow, column=thatDayCol)
            if 'Su' in thatDayName:
                weekRow += 1

        self.weekRowStop = weekRow

    def update(self):
        self.root.after(50, self.update)


app = PlannerApp()
