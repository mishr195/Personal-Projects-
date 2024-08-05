#include "shuffle.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

static void printDeck(CardDeck deck)
{
  int ind;
  for (ind = 0; ind < deck.size; ind ++)
    {
      printf("%c ", deck.cards[ind]);
    }
  printf("\n");
}



void divide(CardDeck origDeck, CardDeck* l_deck, CardDeck* r_deck)
{
    int j;
    for (j = 0; j < origDeck.size - 1; j++)
    {
        strncpy(l_deck[j].cards, origDeck.cards, j + 1);
        l_deck[j].size = j + 1;

        strncpy(r_deck[j].cards, origDeck.cards + j + 1, origDeck.size - (j + 1));
        r_deck[j].size = origDeck.size - (j + 1);
    }
}

// Helper function for interleaving decks
void ilhelper(CardDeck l_deck, CardDeck r_deck, CardDeck currOrder, int currInd, int l_Ind, int r_Ind)
{
    if (l_Ind < l_deck.size)
    {
        currOrder.cards[currInd] = l_deck.cards[l_Ind];
        currOrder.size = currInd + 1;
        ilhelper(l_deck, r_deck, currOrder, currInd + 1, l_Ind + 1, r_Ind);
    }

    if (r_Ind < r_deck.size)
    {
        currOrder.cards[currInd] = r_deck.cards[r_Ind];
        currOrder.size = currInd + 1;
        ilhelper(l_deck, r_deck, currOrder, currInd + 1, l_Ind, r_Ind + 1);
    }

    if (l_Ind == l_deck.size && r_Ind == r_deck.size)
    {
        return;
    }

    if (currOrder.size == l_deck.size + r_deck.size)
    {
        for (int i = 0; i < currOrder.size; i++)
        {
            printf("%c", currOrder.cards[i]);
        }
        printf("\n");
    }
}

// Function to interleave two decks to generate all possible results
void interleave(CardDeck l_deck, CardDeck r_deck)
{
    CardDeck currOrder;
    ilhelper(l_deck, r_deck, currOrder, 0, 0, 0);
}

// Function to shuffle the deck using riffle shuffling
void shuffle(CardDeck origDeck)
{
    int numPairs = origDeck.size - 1;

    if (numPairs == 0)
    {
        return;
    }

    CardDeck *l_deck = NULL;
    CardDeck *r_deck = NULL;

    l_deck = malloc(sizeof(CardDeck) * numPairs);
    r_deck = malloc(sizeof(CardDeck) * numPairs);

    divide(origDeck, l_deck, r_deck);

    int i;
    for (i = 0; i < numPairs; i++)
    {
        interleave(l_deck[i], r_deck[i]);
    }

    free(l_deck);
    free(r_deck);
}