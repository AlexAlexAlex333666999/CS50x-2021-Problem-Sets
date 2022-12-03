// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // Copy a header from an input file to an output file
    uint8_t header[HEADER_SIZE];

    fread(&header[0], HEADER_SIZE, 1, input);
    fwrite(&header[0], HEADER_SIZE, 1, output);

    // Read samples from the input file and write updated data to the output file
    int16_t buffer;

    while (fread(&buffer, sizeof(buffer), 1, input))
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(buffer), 1, output);
        buffer = buffer / factor;
    }

    // Close files
    fclose(input);
    fclose(output);
}
