# Create Node class to hold attributes

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# End Node class

def manhattan(start, end):
    return abs(start[0]-end[0]) + abs(start[1]-end[1])

maze = '''
%%%%%%%%%%%%%%
%.     % %% %%
%%%%%% % %%  %
%    % %     %
% %%   %  %%P%
% %%% %%%%%  %
% %%        %%
%%%%%%%%%%%%%%
'''
start_node = (1, 1)
end_node = (12, 4)

def main():
    print(maze)
    open_list = []
    closed_list = []


if __name__ == '__main__':
    main()

maze_complete = '''
%%%%%%%%%%%%%%
%......% %% %%
%%%%%%.% %%  %
%    %.%     %
% %% ..%  %%P%
% %%%.%%%%%..%
% %% .......%%
%%%%%%%%%%%%%%
'''
