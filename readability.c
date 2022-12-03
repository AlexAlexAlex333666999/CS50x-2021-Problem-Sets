#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <fenv.h>

int main(void)
{

    //counts for letters, words, and sentences
    int letters = 0;
    int words = 0;
    int sent = 0;

    //get a text from a user
    string s = get_string("Text: ");

    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isupper(s[i]) || islower(s[i]))
        {
            letters++;
        }

        else if (isspace(s[i]) && i != 0 && s[i - 1] != '.' && s[i - 1] != '!' && s[i - 1] != '?' && s[i - 1] != ',')
        {
            words++;
        }

        else if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            words++;
            sent++;
        }

        else if (s[i] == ',')
        {
            words++;
        }
    }

//convert letters, words, and sentences into floats
    float let = letters;
    float se = sent;
    float w = words;

//count L and P variables for the Coleman-Liau formula
    float l = let * (100 / w);
    float p = se * (100 / w);

//count the final index
    float index = 0.0588 * l - 0.296 * p - 15.8;

//round the index
    int fin = index + 0.5;

//print results
    if (fin < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (fin >= 16)
    {
        printf("Grade 16+\n");
    }

    else
    {
        printf("Grade %i\n", fin);
    }

}
