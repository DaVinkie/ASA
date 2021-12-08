#!/usr/bin/python3

"""
DESCRIPTION:
    Template code for the Dynamic Programming assignment in the Algorithms in Sequence Analysis course at the VU.
    
INSTRUCTIONS:
    Complete the code (compatible with Python 3!) upload to CodeGrade via corresponding Canvas assignment.

AUTHOR:
    <Name and student ID here!>
"""



import argparse
import pickle



def parse_args():
    "Parses inputs from commandline and returns them as a Namespace object."

    parser = argparse.ArgumentParser(prog = 'python3 align.py',
        formatter_class = argparse.RawTextHelpFormatter, description =
        '  Aligns the first two sequences in a specified FASTA\n'
        '  file with a chosen strategy and parameters.\n'
        '\n'
        'defaults:\n'
        '  strategy = global\n'
        '  substitution matrix = pam250\n'
        '  gap penalty = 2')
        
    parser.add_argument('fasta', help='path to a FASTA formatted input file')
    parser.add_argument('output', nargs='*', 
        help='path to an output file where the alignment is saved\n'
             '  (if a second output file is given,\n'
             '   save the score matrix in there)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help='print the score matrix and alignment on screen', default=False)
    parser.add_argument('-s', '--strategy', dest='strategy',
        choices=['global','semiglobal','local'], default="global")
    parser.add_argument('-m', '--matrix', dest='substitution_matrix',
        choices=['pam250','blosum62','identity'], default='pam250')
    parser.add_argument('-g', '--gap_penalty', dest='gap_penalty', type=int,
        help='must be a positive integer', default=2)

    args = parser.parse_args()

    args.align_out = args.output[0] if args.output else False
    args.matrix_out = args.output[1] if len(args.output) >= 2 else False
                      # Fancy inline if-else statements. Use cautiously!
                      
    if args.gap_penalty <= 0:
        parser.error('gap penalty must be a positive integer')

    return args



def load_substitution_matrix(name):
    "Loads and returns the specified substitution matrix from a pickle (.pkl) file."
    # Substitution matrices have been prepared as nested dictionaries:
    # the score of substituting A for Z can be found with subst['A']['Z']
    # NOTE: Only works if working directory contains the correct folder and file!
    
    with open('substitution_matrices/%s.pkl' % name, 'rb') as f:
        subst = pickle.load(f)
    return subst
    
    

def load_sequences(filepath):
    "Reads a FASTA file and returns the first two sequences it contains."
    
    seq1 = []
    seq2 = []
    with open(filepath,'r') as f:
        for line in f:
            if line.startswith('>'):
                if not seq1:
                    current_seq = seq1
                elif not seq2:
                    current_seq = seq2
                else:
                    break # Stop if a 3rd sequence is encountered
            else:
                current_seq.append(line.strip())
    
    if not seq2:
        raise Exception('Error: Not enough sequences in specified FASTA file.')
    
    seq1 = ''.join(seq1)
    seq2 = ''.join(seq2)
    return seq1, seq2



def align(seq1, seq2, strategy, substitution_matrix, gap_penalty):
    "Do pairwise alignment using the specified strategy and parameters."
    # This function consists of 3 parts:
    #
    #   1) Initialize a score matrix as a "list of lists" of the appropriate length.
    #      Fill in the correct values for the first row and column given the strategy.
    #        (local / semiglobal = 0  --  global = stacking gap penalties)
    #   2) Fill in the rest of the score matrix using Dynamic Programming, accounting
    #      for the selected alignment strategy, substitution matrix and gap penalty.
    #   3) Perform the correct traceback routine on your filled in score matrix.
    #
    # Both the resulting alignment (sequences with gaps and the corresponding score)
    # and the filled in score matrix are returned as outputs.
    #
    # NOTE: You are strongly encouraged to think about how you can reuse (parts of)
    #       your code between steps 2 and 3 for the different strategies!
    
    
    ### 1: Initialize
    M = len(seq1)+1
    N = len(seq2)+1
    score_matrix = []
    for i in range(M):
        row = []
        score_matrix.append(row)
        for j in range(N):
            row.append(0)
    
    if strategy == 'global':
        #####################
        # START CODING HERE #
        #####################
        # Apply end-gap penalties
        for i in range(M):
            score_matrix[i][0] = -(gap_penalty*i)
        for j in range(N):
            score_matrix[0][j] = -(gap_penalty*j)
        # pass    # Change the zeroes in the first row and column to the correct values.

        #####################
        #  END CODING HERE  #
        #####################

    
    
    ### 2: Fill in Score Matrix
 
    #####################
    # START CODING HERE #
    #####################
    def dp_function(seq1, seq2, substitution_matrix, score_matrix, gap_penalty, strategy):
        "Fills in the values of the score_matrix by dynamic programming."
        M = len(seq1)
        N = len(seq2)
        
        for i in range(M):
            for j in range(N):
                prot1, prot2 = get_protein(seq1, seq2, i, j)
                score   = get_score(substitution_matrix, prot1, prot2)
                
                s_left  = score_matrix[i+1][j] - gap_penalty
                s_up    = score_matrix[i][j+1] - gap_penalty
                s_next  = score_matrix[i][j] + score

                if strategy == 'local':
                    s_left, s_up, s_next = set_local(s_left, s_up, s_next)

                score_matrix[i+1][j+1] = max(s_left, s_up, s_next)

        return score_matrix

    def get_protein(seq1, seq2, i, j):
        "Returns the two proteins from the sequences that need to be compared."
        prot1 = seq1[i]
        prot2 = seq2[j]
        return prot1, prot2

    def get_score(substitution_matrix, prot1, prot2):
        "Returns the score of the specified protein alignment from the substitution matrix."
        score = substitution_matrix[prot1][prot2]
        return score

    def set_local(s_left, s_up, s_next):
        "Replace negative values with a hard zero if the strategy is local alignment."
        if s_left < 0: 
            s_left = 0
        if s_up < 0:
            s_up = 0
        if s_next < 0:
            s_next = 0
        return s_left, s_up, s_next

    score_matrix = dp_function(seq1, seq2, substitution_matrix, score_matrix, gap_penalty, strategy)
    
    # for i in range(1,M):
    #     for j in range(1,N):
    #         score_matrix[i][j] = dp_function(...)
            
    #####################
    #  END CODING HERE  #
    #####################   
    
    
    ### 3: Traceback
    
    #####################
    # START CODING HERE #
    #####################   

    def traceback(seq1, seq2, score_matrix, gap_penalty, strategy):

        # print(substitution_matrix['R'])
        M = len(seq1)
        N = len(seq2)

        oob_penalty = -(M*N*gap_penalty) # Prevent algorithm from going out of bounds

        aligned_seq1 = ''
        aligned_seq2 = ''

        # # Test case
        # score_matrix[M][N] = 30
        # score_matrix[M-1][N-1] = 30

        if strategy == 'semiglobal':
            # M, aligned_seq1, aligned_seq2 = semiglobal_init(score_matrix, M, N, seq1, aligned_seq1, aligned_seq2)
            M, N, aligned_seq1, aligned_seq2 = semiglobal_init(score_matrix, M, N, seq1, seq2, aligned_seq1, aligned_seq2)

        if strategy == 'local':
            M, N = local_init(score_matrix)

        align_score = score_matrix[M][N]

        while not( M == 0 and N == 0):
            # s_up, s_left, s_prev = calculate_scores(M, N, score_matrix, oob_penalty)
            # direction = decide_direction(s_up, s_left, s_prev)
            pos_directions = possible_directions(seq1, seq2, M, N, score_matrix, 
                substitution_matrix, gap_penalty, oob_penalty, strategy)
            
            if strategy == 'local':
                if list(pos_directions.values()) == [oob_penalty]*3:
                    break

            direction = decide_direction(pos_directions, oob_penalty)

            aligned_seq1, aligned_seq2, M, N = update_sequence(direction, seq1, seq2, 
                aligned_seq1, aligned_seq2, M, N)

        return aligned_seq1, aligned_seq2, align_score

    def calculate_scores(i, j, score_matrix, oob_penalty):
        "Calculate the scores for the traceback algorithm."
        if j == 0:
            s_left = oob_penalty
        else:
            s_left = score_matrix[i][j-1] 
        if i == 0:
            s_up = oob_penalty
        else:
            s_up = score_matrix[i-1][j]
        
        if i == 0 or j == 0:
            s_prev = oob_penalty
        else:
            s_prev = score_matrix[i-1][j-1]

        return s_up, s_left, s_prev

    def possible_directions(seq1, seq2, i, j, score_matrix, substitution_matrix, gap_penalty, oob_penalty, strategy):
        "For all neighboring cells, decide which of the directions are actually possible."

        pos_directions = {'previous': oob_penalty, 'up': oob_penalty, 'left': oob_penalty}
        p1, p2 = get_protein(seq1, seq2, i-1, j-1)
        score = get_score(substitution_matrix, p1, p2)
        s_up, s_left, s_prev = calculate_scores(i, j, score_matrix, oob_penalty)

        # print(p1, p2, score_matrix[i][j-1] - score_matrix[i][j])
        # print(substitution_matrix[p1][p2])


        if score_matrix[i][j] - score_matrix[i-1][j-1] == score:
            pos_directions['previous'] = s_prev
        if score_matrix[i][j-1] - score_matrix[i][j] == gap_penalty:
            pos_directions['left'] = s_left
        if score_matrix[i-1][j] - score_matrix[i][j] == gap_penalty:
            pos_directions['up'] = s_up

        if strategy == 'semiglobal':
            if i == 0:
                pos_directions['left'] = 0
            if j == 0:
                pos_directions['up'] = 0
        # print(pos_directions)
        return pos_directions

    def decide_direction(pos_directions, oob_penalty):
        "Decide direction based on traceback scores."
        # Order of excecution ensures taking the high-road
        # I made a mistake with regards to the high-road traceback approach. Apparently the score of the
        # cells do not matter, as long as the pathway is possible, where I took a max score approach. This
        # led to taking low roads if the alignment score was better.

        # This is fixed by comparing the values to the oob_penalty and always choosing up if possible.
        if max(pos_directions.values()) == pos_directions['up']:
            direction = 'up'
        elif max(pos_directions.values()) == pos_directions['previous']:
            direction = 'previous'
        else:
            direction = 'left'

        print(pos_directions.items(), oob_penalty)

    
        if (direction == 'previous' or direction == 'left') and pos_directions['up'] != oob_penalty:
            direction = 'up'
            print('changed')
        elif (direction == 'left') and pos_directions['previous'] != oob_penalty:
            direction = 'previous'
            print('changed')

        print(direction)
        return direction

    def update_sequence(direction, seq1, seq2, aligned_seq1, aligned_seq2, i, j):
        "Updates the aligned sequences based on the direction."
        if direction == 'left':
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            j -= 1
        elif direction == 'up':
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
            i -= 1
        else:
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            i -= 1
            j -= 1
        return aligned_seq1, aligned_seq2, i, j

    def semiglobal_init(score_matrix, i, j, seq1, seq2, aligned_seq1, aligned_seq2):

        last_row = score_matrix[i]
        last_col = [row[j] for row in score_matrix]

        max_row = max(last_row)
        max_col = max(last_col)

        if max_col >= max_row: # Upper road
            high_index = last_col.index(max_col)
            tail_length = (len(last_col)-1) - high_index
            for t in range(1, tail_length+1):
                aligned_seq2 = '-' + aligned_seq2
                aligned_seq1 =  seq1[-t] + aligned_seq1
            i = i - tail_length 

        else:
            right_index = last_row[::-1].index(max_row)
            tail_length = right_index
            for t in range(1, tail_length+1):
                aligned_seq1 = '-' + aligned_seq1
                aligned_seq2 =  seq2[-t] + aligned_seq2
            j = j - tail_length

        return i, j, aligned_seq1, aligned_seq2


    def local_init(score_matrix):
        "Initializes the starting position for the traceback routine if the strategy is local alignment."
        score_matrix_transpose = [[row[i] for row in score_matrix] for i in range(len(score_matrix[0]))]
        max_col_values = [max(row) for row in score_matrix_transpose]

        inv_col_index = max_col_values[::-1].index(max(max_col_values))
        j = (len(score_matrix[0])-1) - inv_col_index
        i = score_matrix_transpose[j].index(max(score_matrix_transpose[j]))

        return i, j

    aligned_seq1, aligned_seq2, align_score = traceback(seq1, seq2, score_matrix, gap_penalty, strategy)
    # print('Alignments: ', aligned_seq1, aligned_seq2)

    # aligned_seq1 = 'foot'  # These are dummy values! Change the code so that
    # aligned_seq2 = 'bart'  # aligned_seq1 and _seq2 contain the input sequences
    # align_score = 0        # with gaps inserted at the appropriate positions.

    #####################
    #  END CODING HERE  #
    #####################   


    alignment = (aligned_seq1, aligned_seq2, align_score)
    return (alignment, score_matrix)



def print_score_matrix(s1,s2,mat):
    "Pretty print function for a score matrix."
    
    # Prepend filler characters to seq1 and seq2
    s1 = '-' + s1
    s2 = ' -' + s2
    
    # Print them around the score matrix, in columns of 5 characters
    print(''.join(['%5s' % aa for aa in s2])) # Convert s2 to a list of length 5 strings, then join it back into a string
    for i,row in enumerate(mat):               # Iterate through the rows of your score matrix (and keep count with 'i').
        vals = ['%5i' % val for val in row]    # Convert this row's scores to a list of strings.
        vals.insert(0,'%5s' % s1[i])           # Add this row's character from s2 to the front of the list
        print(''.join(vals))                   # Join the list elements into a single string, and print the line.



def print_alignment(a):
    "Pretty print function for an alignment (and alignment score)."
    
    # Unpack the alignment tuple
    seq1 = a[0]
    seq2 = a[1]
    score = a[2]
    
    # Check which positions are identical
    match = ''
    for i in range(len(seq1)): # Remember: Aligned sequences have the same length!
        match += '|' if seq1[i] == seq2[i] else ' ' # Fancy inline if-else statement. Use cautiously!
            
    # Concatenate lines into a list, and join them together with newline characters.
    print('\n'.join([seq1,match,seq2,'','Score = %i' % score]))



def save_alignment(a,f):
    "Saves two aligned sequences and their alignment score to a file."
    with open(f,'w') as out:
        out.write(a[0] + '\n') # Aligned sequence 1
        out.write(a[1] + '\n') # Aligned sequence 2
        out.write('Score: %i' % a[2]) # Alignment score


    
def save_score_matrix(m,f):
    "Saves a score matrix to a file in tab-separated format."
    with open(f,'w') as out:
        for row in m:
            vals = [str(val) for val in row]
            out.write('\t'.join(vals)+'\n')
    


def main(args = False):
    # Process arguments and load required data
    if not args: args = parse_args()
    
    sub_mat = load_substitution_matrix(args.substitution_matrix)
    seq1, seq2 = load_sequences(args.fasta)

    # Perform specified alignment
    strat = args.strategy
    gp = args.gap_penalty
    alignment, score_matrix = align(seq1, seq2, strat, sub_mat, gp)

    # If running in "verbose" mode, print additional output
    if args.verbose:
        print_score_matrix(seq1,seq2,score_matrix)
        print('') # Insert a blank line in between
        print_alignment(alignment)
    
    # Save results
    if args.align_out: save_alignment(alignment, args.align_out)
    if args.matrix_out: save_score_matrix(score_matrix, args.matrix_out)



if __name__ == '__main__':
    main()