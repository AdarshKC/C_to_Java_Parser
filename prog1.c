#include<stdio.h>

int search(int arr[], unsigned int arr_len, int x){  
    for (unsigned int i = 0; i < arr_len; i++) 
	if (arr[(unsigned int)i] == x) 
	    return (int)i; 
    return -1; 
} 

int factorial(int num);

int verifyFactorial(int num){
    int fact = 1;
    if(num < 0){
    	fact = -1;
    }
    else if(num > 1){ 
	    do{
		fact = fact * num;
		num = num - 1;
	     }while(num>1);
    }
    else {
    	fact = 1;
    }
    return fact;	
}

void main() {
	   int arr[] = { 1, 2, 3, 4, 5, 6 }; 
	   int num = 6; 
	   int result = search(arr, 6, num); 
	   printf("%d\n", result); 
	   result = factorial(num);
	   printf("%d\n", result); 
}

//This should be linked to its function declaration 
int factorial(int num){
    int copyNum = num;
    int fact = 1;
    if(num < 0)
    	fact = -1;
    else{
	while(num > 1){
	    fact = fact * num--;
	}
    }
    return fact==verifyFactorial(copyNum)? fact:-2;
}


