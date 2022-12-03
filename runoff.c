#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j] is jth preference for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// Candidates have name, vote count, eliminated status
typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int voter_count;
int candidate_count;

// Function prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }

    //collect the candidates' names and set it to the candidate.name
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    //get a number of voters
    voter_count = get_int("Number of voters: ");
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++)
    {

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            // Record vote, unless it's invalid
            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }
    return 0;
}

// Record preference if vote is valid. i is voter, j is rank, name is name
bool vote(int voter, int rank, string name)
{
    // k is a candidate index
    for (int k = 0; k < candidate_count; k++)
    {
        if (strcmp(candidates[k].name, name) == 0)
        {
            preferences[voter][rank] = k;
            return true;
        }
    }
    // TODO
    return false;
}

// Tabulate votes for non-eliminated candidates
void tabulate(void)
{
    // count votes
    for (int l = 0; l < voter_count; l++)
    {
        for (int m = 0; m < candidate_count; m++)
        {
            if (preferences[l][0] == m)
            {
                candidates[m].votes++;
            }
        }
    }

    //eliminate the last one
    for (int n = 0; n < candidate_count; n++)
    {
        for (int p = 0; p < candidate_count; p++)
        {
            if (candidates[p].votes == n)
            {
                candidates[p].eliminated = true;
                break;
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    // Find if there is a winner
    for (int q = 0; q < candidate_count; q++)
    {
        if (candidates[q].eliminated == false)
        {
            if (candidates[q].votes >= voter_count / (candidates[q].votes + 0.5))
            {
                printf("%s\n", candidates[q].name);
                return true;
            }
        }
    }

    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    int minimum = candidates[0].votes;

    for (int r = 0; r < candidate_count; r++)
    {
        if (candidates[r].eliminated == false)
        {
            if (candidates[r].votes < minimum)
            {
                minimum = candidates[r].votes;
            }
        }
    }
    return minimum;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    for (int s = 0; s < candidate_count; s++)
    {
        if (candidates[s].eliminated == false)
        {
            if (candidates[s].votes > min)
            {
                return false;
            }
        }
    }
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    for (int t = 0; t < candidate_count; t++)
    {
        if (candidates[t].eliminated == false)
        {
            if (candidates[t].votes == min)
            {
                candidates[t].eliminated = true;
            }
        }
    }

    return;
}
