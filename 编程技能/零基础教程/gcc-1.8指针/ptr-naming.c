#include <stdio.h>

int main() {
    int  a = 10;
    char c = 'A';

    /* 下面 4 个变量，名字完全不同，但类型只由【前面的 int/char】决定 */
    int  *p      = &a;   /* p      是 int 指针 */
    int  *xyz    = &a;   /* xyz    也是 int 指针（名字随便起） */
    char *q      = &c;   /* q      是 char 指针 */
    char *hello  = &c;   /* hello  也是 char 指针 */

    printf("p     指向的值 = %d\n", *p);
    printf("xyz   指向的值 = %d   <- 名字换了，作用一样\n", *xyz);
    printf("q     指向的值 = %c\n", *q);
    printf("hello 指向的值 = %c   <- 名字换了，作用一样\n", *hello);

    printf("\n  int  *p     = p 是【int 指针】\n");
    printf("  char *q     = q 是【char 指针】\n");
    printf("  ⇒ 类型看【前面的 int/char】，名字 p/q 随便起\n");

    return 0;
}
