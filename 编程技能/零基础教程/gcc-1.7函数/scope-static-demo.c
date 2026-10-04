#include <stdio.h>

/* 1.7 第 3 课 · 作用域 + static 验证 */

int g = 100;              /* 全局变量 */

void testStatic() {
    int a = 0;            /* 普通局部变量：每次调用重新变 0 */
    static int b = 0;     /* static 局部变量：只初始化一次，之后记住上次 */
    a++;
    b++;
    printf("   普通 a = %d  |  static b = %d\n", a, b);
}

void testScope() {
    int x = 1;
    {
        int x = 2;        /* 块内另定义 x，遮蔽外层 */
        printf("   块内 x = %d  ← 内层遮蔽了外层\n", x);
    }
    printf("   块外 x = %d  ← 外层没受影响\n", x);
}

void testGlobal() {
    int g = 999;          /* 局部变量，与全局同名 */
    printf("   函数内 g = %d  ← 局部【屏蔽】了全局\n", g);
}

int main() {
    printf("=== 实验 1：static 局部变量「记住上次」 ===\n");
    printf("   调用第 1 次：\n");
    testStatic();
    printf("   调用第 2 次：\n");
    testStatic();
    printf("   调用第 3 次：\n");
    testStatic();

    printf("\n=== 实验 2：复合语句作用域 ===\n");
    testScope();

    printf("\n=== 实验 3：同名屏蔽（就近原则） ===\n");
    printf("   全局 g = %d\n", g);
    testGlobal();
    printf("   函数外再看全局 g = %d  ← 全局没变\n", g);

    return 0;
}
