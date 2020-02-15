#include <stdio.h>
#include <string.h>
/*
  You can write C code here or look at the examples.
  It will be translated as "demo/demo_translation.c".
  There are also translations of full p    rograms below.
*/
int main(int argc, char** argv)
{
  printf("Number of arguments: ");
  printf("%d\n", argc);
  printf("Without program name: ");
  printf("%d\n", argc - 1);
  return 0;
}