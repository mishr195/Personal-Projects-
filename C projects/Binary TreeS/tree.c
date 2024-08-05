#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "tree.h"

// DO NOT MODIFY FROM HERE --->>>
Tree * newTree(void)
{
  Tree * t = malloc(sizeof(Tree));
  t->root = NULL;
  return t;
}

void deleteTreeNode(TreeNode * tr)
{
  if (tr == NULL)
    {
      return;
    }
  deleteTreeNode(tr->left);
  deleteTreeNode(tr->right);
  free(tr);
}

void freeTree(Tree * tr)
{
  if (tr == NULL)
    {
      // nothing to delete
      return;
    }
  deleteTreeNode(tr->root);
  free(tr);
}

// <<<--- UNTIL HERE

// ***
// *** You MUST modify the following functions
// ***

// You ARE allowed to create any helper functions needed
// for either of the following functions

// Helper function to create a new tree node
TreeNode *newTreeNode(int data) {
  TreeNode *newNode = malloc(sizeof(TreeNode));
  if (newNode == NULL) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  newNode->value = data;
  newNode->left = newNode->right = NULL;
  return newNode;
}

// Helper function to search for an element in inArray within given range
int search(int arr[], int strt, int end, int value) {
  int i;
  for (i = strt; i <= end; i++) {
    if (arr[i] == value)
      return i;
  }
  return -1;
}

// Helper function to construct the binary tree recursively
TreeNode *buildUtil(int *inArray, int *postArray, int inStart, int inEnd, int *postIndex) {
  if (inStart > inEnd)
    return NULL;

  TreeNode *root = newTreeNode(postArray[*postIndex]);
  (*postIndex)--;

  if (inStart == inEnd)
    return root;

  int inIndex = search(inArray, inStart, inEnd, root->value);

  root->right = buildUtil(inArray, postArray, inIndex + 1, inEnd, postIndex);
  root->left = buildUtil(inArray, postArray, inStart, inIndex - 1, postIndex);

  return root;
}

/*
buildTree:
Given the infix (inArray), postfix (postArray), and size
of a binary tree, construct a binary tree
Note that this tree is not necessarily a binary search tree
*/
Tree *buildTree(int *inArray, int *postArray, int size)
{
  Tree *tree = newTree();
  int postIndex = size - 1;
  tree->root = buildUtil(inArray, postArray, 0, size - 1, &postIndex);
  return tree;
}

// Helper function to print the path from a node to root
bool printPathUtil(TreeNode *root, int val) {
  if (root == NULL)
    return false;

  if (root->value == val || printPathUtil(root->left, val) || printPathUtil(root->right, val)) {
    printf("%d\n", root->value);
    return true;
  }
  return false;
}

/*
printPath:
Print the path from the desired node to the root, inclusive at both
ends with the root being printed last
*/
void printPath(Tree *tr, int val)
{
  if (tr == NULL || tr->root == NULL) {
    printf("No Path\n");
    return;
  }
  if (!printPathUtil(tr->root, val))
    printf("No Path\n");
  else
    printf("\n");
}
