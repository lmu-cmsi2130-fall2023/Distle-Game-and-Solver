from typing import *
'''
Variety of functions related to computing the edit distance between
strings and, importantly, which WILL be used by the DistleGame to
provide feedback to the DistlePlayer during a game of Distle.

[!] Feel free to use any of these methods as needed in your DistlePlayer.

[!] Feel free to ADD any methods you see fit for use by your DistlePlayer,
e.g., some form of entropy computation.
'''

def get_edit_dist_table(row_str: str, col_str: str) -> list[list[int]]:
    '''
    Returns the completed Edit Distance memoization structure: a 2D list
    of ints representing the number of string manupulations required to
    minimally turn each subproblem's string into the other.
    
    Parameters:
        row_str (str):
            The string located along the table's rows
        col_str (col):
            The string located along the table's columns
    
    Returns:
        list[list[int]]:
            Completed memoization table for the computation of the
            edit_distance(row_str, col_str)
    '''
    # [!] TODO

    table: list[list[int]] = []

    for _ in range(len(row_str) + 1):
        row: list = []
        for _ in range(len(col_str) + 1):
            row.append(0)
        table.append(row)

    for r in range(len(row_str) + 1):
        table[r][0] = r
    for c in range(len(col_str) + 1):
        table[0][c] = c

    for r in range(1, len(row_str) + 1):
        for c in range(1, len(col_str) + 1):

            deletion = replacement = transposition = insertion = 1000

            if c >= 1:
                insertion = table[r][c-1] + 1
            if r >= 1:
                deletion = table[r-1][c] + 1
            if row_str[r-1] == col_str[c-1] and r >= 1 and c >= 1:
                replacement = table[r-1][c-1]
            if row_str[r-1] != col_str[c-1] and r >= 1 and c >= 1:
                replacement = table[r-1][c-1] + 1
            if row_str[r-1] == col_str[c-2] and row_str[r-2] == col_str[c-1] and r >= 2 and c>= 2:
                transposition = table[r-2][c-2] + 1
            table[r][c] = min (deletion, replacement, insertion, transposition)
    return table

def edit_distance(s0: str, s1: str) -> int:
    '''
    Returns the edit distance between two given strings, defined as an
    int that counts the number of primitive string manipulations (i.e.,
    Insertions, Deletions, Replacements, and Transpositions) minimally
    required to turn one string into the other.
    
    [!] Given as part of the skeleton, no need to modify
    
    Parameters:
        s0, s1 (str):
            The strings to compute the edit distance between
    
    Returns:
        int:
            The minimal number of string manipulations
    '''
    if s0 == s1: return 0
    return get_edit_dist_table(s0, s1)[len(s0)][len(s1)]

def get_transformation_list(s0: str, s1: str) -> list[str]:
    '''
    Returns one possible sequence of transformations that turns String s0
    into s1. The list is in top-down order (i.e., starting from the largest
    subproblem in the memoization structure) and consists of Strings representing
    the String manipulations of:
        1. "R" = Replacement
        2. "T" = Transposition
        3. "I" = Insertion
        4. "D" = Deletion
    In case of multiple minimal edit distance sequences, returns a list with
    ties in manipulations broken by the order listed above (i.e., replacements
    preferred over transpositions, which in turn are preferred over insertions, etc.)
    
    [!] Given as part of the skeleton, no need to modify
    
    Example:
        s0 = "hack"
        s1 = "fkc"
        get_transformation_list(s0, s1) => ["T", "R", "D"]
        get_transformation_list(s1, s0) => ["T", "R", "I"]
    
    Parameters:
        s0, s1 (str):
            Start and destination strings for the transformation
    
    Returns:
        list[str]:
            The sequence of top-down manipulations required to turn s0 into s1
    '''
    
    return get_transformation_list_with_table(s0, s1, get_edit_dist_table(s0, s1))

def get_transformation_list_with_table(s0: str, s1: str, table: list[list[int]]) -> list[str]:
    '''
    See get_transformation_list documentation.
    
    This method does exactly the same thing as get_transformation_list, except that
    the memoization table is input as a parameter. This version of the method can be
    used to save computational efficiency if the memoization table was pre-computed
    and is being used by multiple methods.
    
    [!] MUST use the already-solved memoization table and must NOT recompute it.
    [!] MUST be implemented recursively (i.e., in top-down fashion)
    '''
    # [!] TODO

    final_list: list[str] = []
    r: int = len(s0)
    c: int = len(s1) 

    def do_stuff(c: int, r: int, temp_list: List[str]) -> Optional[List[str]]:
        if table[r][c] == 0:
            return temp_list[::-1]

        temp_R = temp_T = temp_I = temp_D = float('inf')

        if c > 0:
            temp_I = table[r][c-1] 
        if r > 0:
            temp_D = table[r-1][c]
        if c > 0 and r > 0:
            if s0[r-1] == s1[c-1]:
                temp_R = table[r-1][c-1]
            else:
                temp_R = table[r-1][c-1] 
        if c >= 2 and r >= 2 and s0[r-1] == s1[c-2] and s0[r-2] == s1[c-1]:
            temp_T = table[r-2][c-2]  

        minimum = min(temp_T, temp_R, temp_D, temp_I)
        
        if temp_R == minimum:
          if temp_R == table[r][c]:
            do_stuff(c - 1, r - 1, temp_list)
          else:
            temp_list.append("R")
            do_stuff(c - 1, r - 1, temp_list)
        elif temp_T == minimum:
          if temp_T == table[r][c]:
            do_stuff(c - 2, r - 2, temp_list)
          else:
            temp_list.append("T")
            do_stuff(c - 2, r - 2, temp_list)
        elif temp_I == minimum:
          if temp_I == table[r][c]:
            do_stuff(c - 1, r, temp_list)
          else:
            temp_list.append("I")
            do_stuff(c - 1, r, temp_list)
        elif temp_D == minimum:
          if temp_D == table[r][c]:
            do_stuff(c, r - 1, temp_list)
          else:
            temp_list.append("D")
            do_stuff(c, r - 1, temp_list)
        return None

    do_stuff(c, r, final_list)
    return final_list


