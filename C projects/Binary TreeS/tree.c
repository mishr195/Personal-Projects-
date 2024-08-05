// ***
// *** You MUST modify this file
// ***

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tree.h"

// DO NOT MODIFY FROM HERE --->>>
void deleteTreeNode(TreeNode * tr)
{
  if (tr == NULL)
    {
      return;
    }
  deleteTreeNode (tr -> left);
  deleteTreeNode (tr -> right);
  free (tr);
}

void freeTree(Tree * tr)
{
  if (tr == NULL)
    {
      // nothing to delete
      return;
    }
  deleteTreeNode (tr -> root);
  free (tr);
}

static void preOrderNode(TreeNode * tn, FILE * fptr)
{
  if (tn == NULL)
    {
      return;
    }
  fprintf(fptr, "%d\n", tn -> value);
  preOrderNode(tn -> left, fptr);
  preOrderNode(tn -> right, fptr);
}

void preOrder(Tree * tr, char * filename)
{
  if (tr == NULL)
    {
      return;
    }
  FILE * fptr = fopen(filename, "w");
  preOrderNode(tr -> root, fptr);
  fclose (fptr);
}
// <<<--- UNTIL HERE

// ***
// *** You MUST modify the follow function
// ***

// Consider the algorithm posted on
// https://www.geeksforgeeks.org/construct-a-binary-tree-from-postorder-and-inorder/

TreeNode* buildTreeHelper(int* inArray, int* postArray, int inStart, int inEnd, int postStart, int postEnd) {
    // Base case: if indices are invalid or there are no elements in the subtree
    if (inStart > inEnd || postStart > postEnd) {
        return NULL;
    }

    // Create a new node with the value from the last element of the postorder array
    TreeNode* root = (TreeNode*)malloc(sizeof(TreeNode));
    root->value = postArray[postEnd];
    root->left = root->right = NULL;

    // Find the index of the root node in inorder array
    int rootIndex;
    for (rootIndex = inStart; rootIndex <= inEnd; rootIndex++) {
        if (inArray[rootIndex] == root->value) {
            break;
        }
    }

    // Calculate the size of the left subtree
    int leftSubtreeSize = rootIndex - inStart;

    // Recursively build left and right subtrees
    root->left = buildTreeHelper(inArray, postArray, inStart, rootIndex - 1, postStart, postStart + leftSubtreeSize - 1);
    root->right = buildTreeHelper(inArray, postArray, rootIndex + 1, inEnd, postStart + leftSubtreeSize, postEnd - 1);

    return root;
}

// Function to construct binary tree from inorder and postorder arrays
Tree* buildTree(int* inArray, int* postArray, int size) {
    if (inArray == NULL || postArray == NULL || size <= 0) {
        return NULL;
    }
    Tree* tree = (Tree*)malloc(sizeof(Tree));
    tree->root = buildTreeHelper(inArray, postArray, 0, size - 1, 0, size - 1);
    return tree;
}
