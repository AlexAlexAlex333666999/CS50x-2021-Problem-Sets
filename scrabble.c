#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char UPPER[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
char LOWER[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }

    else
    {
        printf("Tie!\n");
    }
}


int compute_score(string word)
{
    // Compute and return score for string
    int current = 0;
    int score = 0;

    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (isupper(word[i]))
        {
            for (int q = 0; q < 26; q++)
            {
                if (word[i] == UPPER[q])
                {
                    current = POINTS[q];
                    score = score + current;
                }

            }
        }

        else if islower(word[i])
        {
            for (int r = 0; r < 26; r++)
            {
                if (word[i] == LOWER[r])
                {
                    current = POINTS[r];
                    score = score + current;
                }
            }
        }

        //No points for non-letters
        else
        {
            score = score + 0;
        }
    }
    return score;
}
