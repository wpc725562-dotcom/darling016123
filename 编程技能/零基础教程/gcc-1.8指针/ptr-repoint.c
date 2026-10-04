#include <stdio.h>

int main() {
    int a = 10, b = 20;
    int *p = &a;          /* p 这张纸条，先写着 a 的编号 */

    printf("① p 指向 a：*p = %d\n", *p);

    p = &b;               /* 把纸条擦掉，改写成 b 的编号 */
    printf("② p 改指 b：*p = %d   <- 纸条换了一张\n", *p);

    p = &a;               /* 又改回 a */
    printf("③ p 又指回 a：*p = %d\n", *p);

    printf("\n  a 的编号 = %p\n", (void*)&a);
    printf("  b 的编号 = %p\n", (void*)&b);
    printf("  p 现在存的编号 = %p   <- 和 a 一样\n", (void*)p);

    return 0;
}
