#include <stdio.h>

/* ① 值传递：交换不了！ */
void swap_by_value(int x, int y) {
    int t = x; x = y; y = t;
}

/* ② 传址调用：能交换！ */
void swap_by_pointer(int *px, int *py) {
    int t = *px; *px = *py; *py = t;
}

int main() {
    int a = 10, b = 20;

    printf("=== ① 值传递（swap_by_value）===\n");
    printf("  调用前: a=%d b=%d\n", a, b);
    swap_by_value(a, b);
    printf("  调用后: a=%d b=%d   <- 没变！因为只传了复印件\n", a, b);

    printf("\n=== ② 传址调用（swap_by_pointer）===\n");
    printf("  调用前: a=%d b=%d\n", a, b);
    swap_by_pointer(&a, &b);
    printf("  调用后: a=%d b=%d   <- 变了！因为传的是门牌号\n", a, b);

    printf("\n=== ③ 逐字拆解 ===\n");
    printf("  swap_by_pointer(&a, &b);\n");
    printf("                    ↑   ↑\n");
    printf("                   传的是【地址】，不是值\n");
    printf("  函数里 int *px = &a;  ⇒ *px 就是 a 本人\n");

    return 0;
}
