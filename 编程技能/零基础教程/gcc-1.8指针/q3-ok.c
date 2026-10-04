#include <stdio.h>
int main() {
    int a = 10;
    int *p = &a;
    *p = a;              /* *p 是 int，a 也是 int ⇒ 合法 */
    printf("*p = a 之后: a = %d, *p = %d\n", a, *p);
    *p = 99;             /* 换个值试试 */
    printf("*p = 99 之后: a = %d\n", a);
    return 0;
}
