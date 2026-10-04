#include <stdio.h>
int main() {
    int a[3] = {5, 10, 15};
    int *p = a;              /* ← 这里 p 已经有初值了！ */
    printf("  *p = %d   ← 能取出来，值是 5\n", *p);
    printf("  p 指向 a[0]，因为 p = a = &a[0]\n");
    return 0;
}
