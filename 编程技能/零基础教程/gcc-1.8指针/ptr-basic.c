#include <stdio.h>

int main() {
    int a = 10;
    int *p = &a;          /* p 存的是 a 的地址 */

    printf("a 的值       = %d\n", a);
    printf("&a 的地址    = %p\n", (void*)&a);
    printf("p 里存的值   = %p   <- 和 &a 一样\n", (void*)p);
    printf("*p 取出的值  = %d   <- 就是 a\n", *p);
    printf("\n");

    /* 通过指针改 a */
    *p = 99;
    printf("执行 *p = 99 之后，a = %d\n", a);

    /* *&a == a（互逆操作） */
    printf("*&a          = %d   <- 还是 a\n", *&a);

    return 0;
}
