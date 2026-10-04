#include <stdio.h>

int main() {
    int a[3] = {5, 10, 15};

    printf("=== ① 数组名 a 到底是什么？ ===\n");
    printf("  a        = %p   <- 数组名自己的值\n", (void*)a);
    printf("  &a[0]    = %p   <- 第 0 个元素的地址\n", (void*)&a[0]);
    printf("  &a       = %p   <- 整个数组的地址（值一样，但含义不同）\n", (void*)&a);
    printf("  ⇒ a 和 &a[0] 【完全相等】⇒ 数组名 = 首元素地址\n");

    printf("\n=== ② 所以 int *p = a; 为什么合法 ===\n");
    int *p = a;    /* 把「首元素地址」交给 p */
    printf("  p = a 之后，*p = %d   <- 就是 a[0]\n", *p);

    printf("\n=== ③ a[i] 和 *(a+i) 完全等价 ===\n");
    for (int i = 0; i < 3; i++)
        printf("  a[%d]=%d  *(a+%d)=%d  %s\n", i, a[i], i, *(a+i),
               (a[i] == *(a+i)) ? "等价" : "不等价");

    printf("\n=== ④ a[3] 越界会怎样（下标只能 0-2）===\n");
    printf("  合法下标只有 0、1、2\n");
    printf("  a[3] 是【越界】读取 —— 值不确定（可能是任何垃圾数）\n");
    printf("  ⇒ 考试里这种题要答「越界 / 未定义」，不能算具体值\n");

    return 0;
}
