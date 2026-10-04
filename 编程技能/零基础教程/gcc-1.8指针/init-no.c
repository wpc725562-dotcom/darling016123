#include <stdio.h>
int main() {
    int *p;                  /* ← 只声明，没赋值 */
    printf("  p 里现在是 %p（随机垃圾值）\n", (void*)p);
    printf("  ⇒ 这个 p 叫【野指针】，*p 可能崩溃\n");
    return 0;
}
