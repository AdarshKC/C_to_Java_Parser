int max(int x, int y)
{
	if(x > y)
	return y;

	return x;
}

/*
  You can write C code here or look at the examples.
  It will be translated as "demo/demo_translation.c".
  There are also translations of full programs below.
*/
void main(int argc, char** argv)
{
	int i = 2, j = 2, k =2;
	if(2 >1)
		{printf("true");}
	else {printf("false");}
	while (j>i)
	{j=j-1;
	i=i+1;}
	printf("Value of this %d And done.\n", i+j+k);
	printf("Value of argument %d And done.\n", argc);
	printf("Value of this %d And done.\n", i+j+k);

}
