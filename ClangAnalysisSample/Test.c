#include <stdio.h>
#include <stdlib.h>


/* 这里有两个函数声明 
    */
int fun1();
int fun2();
   /*
 这里是注释
       */

int main(){
    int i , *j = 1;
    int m, n;
    i = 0;
    m = fun1(i, *j);
    n = fun2(i, j);
    printf("Hello World!\n");
    printf("EVANZONE\n");
    printf("EvanZone is a sexy boy!\n");
    printf("He codes well\n");
    printf("He loves everything about novel and advanced technology!\n");
    printf("And He is smart to understand anything in a while\n");
    printf("All above is just his Dream😂\n");
    return 0;
}

// 这是一个
int fun1(int A, int B){
    return A+B;
}

int fun2(int C, int *D){
    int i = 0;
    for (i = 0; i < 10; i++){
        printf("%d\n", i);
    }
    return C*C + *D;
}

void fun3
(
    void * A
    , 
    void *B
)
{
    printf("This is fun3!\n"); // 这里又是一个注释
}
