import os
TOP = os.path.dirname(os.path.abspath(__file__))
SKATER_WIN_DATA = os.path.join(TOP, 'skaterwindata', 'queues')

if __name__=='__main__':
    print(TOP)
