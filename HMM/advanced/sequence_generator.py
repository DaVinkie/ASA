#!/usr/bin/python3

"""
DESCRIPTION:
    Template code for the FIRST Advanced Question of the Hidden Markov Models
    assignment in the Algorithms in Sequence Analysis course at the VU.

INSTRUCTIONS:
    Complete the code (compatible with Python 3!) upload to CodeGrade via
    corresponding Canvas assignment. Note this script will be graded manually,
    if and only if your "hmm.py" script succesfully implements Baum-Welch
    training! Continuous Feedback will not be available for this script.

AUTHOR:
    Daniël Vink (2715294)
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from hmm_utility import load_tsv
from numpy.random import choice



def parse_args():
    #####################
    # START CODING HERE #
    #####################
    # Implement a simple argument parser (WITH help documentation!) that parses
    # the information needed by main() from commandline. Take a look at the
    # argparse documentation, the parser in hmm_utility.py or align.py
    # (from the Dynamic Programming exercise) for hints on how to do this.

    parser = ArgumentParser(prog = 'python3 sequence_generator.py',
        formatter_class = RawTextHelpFormatter, description = 
        '''
            Generate a specified amount of sequences from a given transition and emission matrices.
            Example syntax: \n
                python3 sequence_generator.py -n 100 -o output A.tsv E.tsv
        ''')

    parser.add_argument('-o', dest='out', default='sequence', help='Name of output file')
    parser.add_argument('-n', dest='amount', type=int, default=10, help='Amount of sequences to generate')
    parser.add_argument('transition', help='path to a TSV formatted transition matrix')
    parser.add_argument('emission', help='path to a TSV formatted emission matrix')
    # parser.add_argument(?)

    return parser.parse_args()
    
    #####################
    #  END CODING HERE  #
    #####################


def generate_sequence(A,E):
    #####################
    # START CODING HERE #
    #####################
    # Implement a function that generates a random sequence using the choice()
    # function, given a Transition and Emission matrix.
    
    # Look up its documentation online:
    # https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.choice.html
    
    sequence = '-'
    state = 'B'
    while True:
        state = choice(list(A[state].keys()), 1, p=list(A[state].values()))[0]
        if state == 'E': 
            break
        else:
            char = choice(list(E[state].keys()), 1, p=list(E[state].values()))[0]
            sequence = sequence + char

    sequence = sequence[1:]



    #####################
    #  END CODING HERE  #
    #####################
    
    return sequence



def main():
    args = parse_args()
    #####################
    # START CODING HERE #
    #####################
    # Uncomment and complete (i.e. replace '?' in) the lines below:
    
    N = args.amount                 # The number of sequences to generate
    out_file = args.out + '.fasta'  # The file path to which to save the sequences
    A = load_tsv(args.transition)   # Transition matrix
    E = load_tsv(args.emission)     # Emission matrix

    with open(out_file,'w') as f:
        for i in range(N):
            seq = generate_sequence(A, E)
            f.write('>random_sequence_%i\n%s\n' % (i,seq))
        
    # generate_sequence(A, E)
    # print(A['B'].keys(), A['B'].values())
    #####################
    #  END CODING HERE  #
    #####################
    


if __name__ == "__main__":
    main()
