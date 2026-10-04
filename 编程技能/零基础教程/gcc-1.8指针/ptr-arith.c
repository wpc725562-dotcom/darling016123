#include <stdio.h>

int main() {
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a;              /* 数组名 a = 首元素的地址 */

    printf("=== ① 指针 + 整数：p+1 走多远？ ===\n");
    printf("  p   存的地址 = %p   指向的值 = %d\n", (void*)p, *p);
    printf("  p+1 存的地址 = %p   指向的值 = %d\n", (void*)(p+1), *(p+1));
    printf("  ⇒ 地址差 = %d 字节（一个 int 的宽度，不是 1 字节！）\n", (int)((char*)(p+1) - (char*)p));

    printf("\n=== ② 两种写法等价：*(p+i) 就是 a[i] ===\n");
    for (int i = 0; i < 5; i++)
        printf("  a[%d]=%d  *(p+%d)=%d  %s\n", i, a[i], i, *(p+i),
               (a[i] == *(p+i)) ? "等价" : "不等价");

    printf("\n=== ③ *(p++) 和 *p++ 是一回事 ===\n");
    int *q = a;
    printf("  *q++ 取出 = %d（先取值，再挪指针）\n", *q++);
    printf("  现在 q 指向 = %d\n", *q);
    printf("  *q++ 取出 = %d\n", *q++);
    printf("  现在 q 指向 = %d\n", *q);

    return 0;
}
